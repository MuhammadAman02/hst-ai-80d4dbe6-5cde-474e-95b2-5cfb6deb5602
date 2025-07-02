"""Social service for connections, posts, and interactions."""

from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, and_, or_, desc
from typing import Optional, List
from app.models.social import Connection, ConnectionStatus, Post, Comment, Like
from app.models.user import User
from app.schemas.social import ConnectionCreate, PostCreate, CommentCreate
from app.core.logging import get_logger

logger = get_logger("social_service")

class SocialService:
    """Service for social networking operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Connection methods
    def send_connection_request(self, requester_id: int, connection_create: ConnectionCreate) -> Optional[Connection]:
        """Send a connection request."""
        try:
            # Check if connection already exists
            stmt = select(Connection).where(
                or_(
                    and_(Connection.requester_id == requester_id, Connection.addressee_id == connection_create.addressee_id),
                    and_(Connection.requester_id == connection_create.addressee_id, Connection.addressee_id == requester_id)
                )
            )
            existing_connection = self.db.execute(stmt).scalar_one_or_none()
            
            if existing_connection:
                logger.warning(f"Connection already exists between {requester_id} and {connection_create.addressee_id}")
                return None
            
            # Create new connection request
            connection = Connection(
                requester_id=requester_id,
                addressee_id=connection_create.addressee_id,
                message=connection_create.message,
                status=ConnectionStatus.PENDING
            )
            
            self.db.add(connection)
            self.db.commit()
            self.db.refresh(connection)
            
            logger.info(f"Connection request sent from {requester_id} to {connection_create.addressee_id}")
            return connection
            
        except Exception as e:
            logger.error(f"Error sending connection request: {e}")
            self.db.rollback()
            return None
    
    def respond_to_connection(self, connection_id: int, user_id: int, accept: bool) -> Optional[Connection]:
        """Accept or decline a connection request."""
        try:
            connection = self.db.get(Connection, connection_id)
            
            if not connection or connection.addressee_id != user_id:
                logger.warning(f"Invalid connection response attempt by user {user_id}")
                return None
            
            connection.status = ConnectionStatus.ACCEPTED if accept else ConnectionStatus.DECLINED
            self.db.commit()
            self.db.refresh(connection)
            
            logger.info(f"Connection {connection_id} {'accepted' if accept else 'declined'} by user {user_id}")
            return connection
            
        except Exception as e:
            logger.error(f"Error responding to connection: {e}")
            self.db.rollback()
            return None
    
    def get_user_connections(self, user_id: int) -> List[Connection]:
        """Get all accepted connections for a user."""
        try:
            stmt = select(Connection).where(
                and_(
                    or_(Connection.requester_id == user_id, Connection.addressee_id == user_id),
                    Connection.status == ConnectionStatus.ACCEPTED
                )
            ).options(
                selectinload(Connection.requester),
                selectinload(Connection.addressee)
            )
            
            result = self.db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting connections for user {user_id}: {e}")
            return []
    
    def get_pending_requests(self, user_id: int) -> List[Connection]:
        """Get pending connection requests for a user."""
        try:
            stmt = select(Connection).where(
                and_(
                    Connection.addressee_id == user_id,
                    Connection.status == ConnectionStatus.PENDING
                )
            ).options(selectinload(Connection.requester))
            
            result = self.db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting pending requests for user {user_id}: {e}")
            return []
    
    # Post methods
    def create_post(self, user_id: int, post_create: PostCreate) -> Optional[Post]:
        """Create a new post."""
        try:
            post = Post(
                user_id=user_id,
                content=post_create.content
            )
            
            self.db.add(post)
            self.db.commit()
            self.db.refresh(post)
            
            logger.info(f"Post created by user {user_id}")
            return post
            
        except Exception as e:
            logger.error(f"Error creating post for user {user_id}: {e}")
            self.db.rollback()
            return None
    
    def get_user_posts(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Post]:
        """Get posts by a specific user."""
        try:
            stmt = select(Post).where(Post.user_id == user_id).order_by(desc(Post.created_at)).offset(skip).limit(limit)
            stmt = stmt.options(
                selectinload(Post.author),
                selectinload(Post.comments).selectinload(Comment.author),
                selectinload(Post.likes).selectinload(Like.user)
            )
            
            result = self.db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting posts for user {user_id}: {e}")
            return []
    
    def get_feed(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Post]:
        """Get feed posts for a user (posts from connections)."""
        try:
            # Get user's connections
            connections = self.get_user_connections(user_id)
            connected_user_ids = []
            
            for conn in connections:
                if conn.requester_id == user_id:
                    connected_user_ids.append(conn.addressee_id)
                else:
                    connected_user_ids.append(conn.requester_id)
            
            # Include user's own posts
            connected_user_ids.append(user_id)
            
            # Get posts from connected users
            stmt = select(Post).where(Post.user_id.in_(connected_user_ids)).order_by(desc(Post.created_at)).offset(skip).limit(limit)
            stmt = stmt.options(
                selectinload(Post.author),
                selectinload(Post.comments).selectinload(Comment.author),
                selectinload(Post.likes).selectinload(Like.user)
            )
            
            result = self.db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting feed for user {user_id}: {e}")
            return []
    
    # Interaction methods
    def like_post(self, user_id: int, post_id: int) -> Optional[Like]:
        """Like a post."""
        try:
            # Check if already liked
            stmt = select(Like).where(and_(Like.user_id == user_id, Like.post_id == post_id))
            existing_like = self.db.execute(stmt).scalar_one_or_none()
            
            if existing_like:
                # Unlike the post
                self.db.delete(existing_like)
                self.db.commit()
                logger.info(f"Post {post_id} unliked by user {user_id}")
                return None
            
            # Create new like
            like = Like(user_id=user_id, post_id=post_id)
            self.db.add(like)
            self.db.commit()
            self.db.refresh(like)
            
            logger.info(f"Post {post_id} liked by user {user_id}")
            return like
            
        except Exception as e:
            logger.error(f"Error liking post {post_id} by user {user_id}: {e}")
            self.db.rollback()
            return None
    
    def comment_on_post(self, user_id: int, post_id: int, comment_create: CommentCreate) -> Optional[Comment]:
        """Comment on a post."""
        try:
            comment = Comment(
                user_id=user_id,
                post_id=post_id,
                content=comment_create.content
            )
            
            self.db.add(comment)
            self.db.commit()
            self.db.refresh(comment)
            
            logger.info(f"Comment added to post {post_id} by user {user_id}")
            return comment
            
        except Exception as e:
            logger.error(f"Error commenting on post {post_id} by user {user_id}: {e}")
            self.db.rollback()
            return None

__all__ = ["SocialService"]