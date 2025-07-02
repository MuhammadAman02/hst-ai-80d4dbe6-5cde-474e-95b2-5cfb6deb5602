"""Main NiceGUI application with LinkedIn clone interface."""

from nicegui import ui, app
from typing import Optional, Dict, Any, List
import asyncio
from datetime import datetime, date
import os
from pathlib import Path

# Import services and models
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.profile_service import ProfileService
from app.services.social_service import SocialService
from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserUpdate
from app.schemas.profile import ExperienceCreate, EducationCreate, SkillCreate
from app.schemas.social import PostCreate, CommentCreate, ConnectionCreate
from app.models.user import User
from app.models.social import Post, Connection, ConnectionStatus
from app.core.logging import get_logger

logger = get_logger("main_ui")

# Global state management
class AppState:
    def __init__(self):
        self.current_user: Optional[User] = None
        self.db_session = None
        self.auth_service = None
        self.user_service = None
        self.profile_service = None
        self.social_service = None
    
    def initialize_services(self):
        """Initialize database services."""
        try:
            self.db_session = next(get_db())
            self.auth_service = AuthService(self.db_session)
            self.user_service = UserService(self.db_session)
            self.profile_service = ProfileService(self.db_session)
            self.social_service = SocialService(self.db_session)
        except Exception as e:
            logger.error(f"Error initializing services: {e}")
    
    def login(self, user: User):
        """Set current user."""
        self.current_user = user
        logger.info(f"User logged in: {user.email}")
    
    def logout(self):
        """Clear current user."""
        if self.current_user:
            logger.info(f"User logged out: {self.current_user.email}")
        self.current_user = None

# Global app state
state = AppState()

# Utility functions
def format_date(date_obj: date) -> str:
    """Format date for display."""
    if date_obj:
        return date_obj.strftime("%B %Y")
    return "Present"

def time_ago(dt: datetime) -> str:
    """Calculate time ago from datetime."""
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    else:
        return "Just now"

# Authentication components
def create_auth_dialog():
    """Create authentication dialog."""
    with ui.dialog() as auth_dialog, ui.card().classes('w-96 p-6'):
        ui.label('Welcome to LinkedIn Clone').classes('text-2xl font-bold mb-4 text-center')
        
        with ui.tabs().classes('w-full') as tabs:
            login_tab = ui.tab('Login')
            register_tab = ui.tab('Register')
        
        with ui.tab_panels(tabs, value=login_tab):
            # Login panel
            with ui.tab_panel(login_tab):
                ui.label('Sign In').classes('text-xl font-semibold mb-4')
                
                email_input = ui.input('Email', placeholder='Enter your email').classes('w-full mb-2')
                password_input = ui.input('Password', placeholder='Enter your password', password=True).classes('w-full mb-4')
                
                async def handle_login():
                    try:
                        if not state.auth_service:
                            state.initialize_services()
                        
                        user_login = UserLogin(email=email_input.value, password=password_input.value)
                        user = state.auth_service.authenticate_user(user_login)
                        
                        if user:
                            state.login(user)
                            auth_dialog.close()
                            ui.notify(f'Welcome back, {user.first_name}!', type='positive')
                            ui.open('/dashboard')
                        else:
                            ui.notify('Invalid credentials', type='negative')
                    except Exception as e:
                        logger.error(f"Login error: {e}")
                        ui.notify('Login failed', type='negative')
                
                ui.button('Sign In', on_click=handle_login).classes('w-full bg-blue-600 text-white')
            
            # Register panel
            with ui.tab_panel(register_tab):
                ui.label('Create Account').classes('text-xl font-semibold mb-4')
                
                first_name_input = ui.input('First Name', placeholder='Enter your first name').classes('w-full mb-2')
                last_name_input = ui.input('Last Name', placeholder='Enter your last name').classes('w-full mb-2')
                reg_email_input = ui.input('Email', placeholder='Enter your email').classes('w-full mb-2')
                reg_password_input = ui.input('Password', placeholder='Create a password', password=True).classes('w-full mb-4')
                
                async def handle_register():
                    try:
                        if not state.auth_service:
                            state.initialize_services()
                        
                        user_create = UserCreate(
                            email=reg_email_input.value,
                            password=reg_password_input.value,
                            first_name=first_name_input.value,
                            last_name=last_name_input.value
                        )
                        
                        user = state.auth_service.register_user(user_create)
                        
                        if user:
                            state.login(user)
                            auth_dialog.close()
                            ui.notify(f'Welcome to LinkedIn Clone, {user.first_name}!', type='positive')
                            ui.open('/profile')
                        else:
                            ui.notify('Registration failed - email may already exist', type='negative')
                    except Exception as e:
                        logger.error(f"Registration error: {e}")
                        ui.notify('Registration failed', type='negative')
                
                ui.button('Create Account', on_click=handle_register).classes('w-full bg-green-600 text-white')
    
    return auth_dialog

# Navigation components
def create_navbar():
    """Create navigation bar."""
    with ui.header().classes('bg-blue-700 text-white shadow-lg'):
        with ui.row().classes('w-full items-center justify-between px-4'):
            # Logo and brand
            with ui.row().classes('items-center'):
                ui.icon('business', size='2rem').classes('mr-2')
                ui.label('LinkedIn Clone').classes('text-xl font-bold cursor-pointer').on('click', lambda: ui.open('/'))
            
            # Navigation links
            if state.current_user:
                with ui.row().classes('items-center space-x-4'):
                    ui.button('Feed', icon='home', on_click=lambda: ui.open('/dashboard')).classes('text-white hover:bg-blue-600').props('flat')
                    ui.button('My Network', icon='people', on_click=lambda: ui.open('/network')).classes('text-white hover:bg-blue-600').props('flat')
                    ui.button('Profile', icon='person', on_click=lambda: ui.open('/profile')).classes('text-white hover:bg-blue-600').props('flat')
                    
                    # User menu
                    with ui.button(icon='account_circle').classes('text-white hover:bg-blue-600').props('flat'):
                        with ui.menu():
                            ui.menu_item(f'Signed in as {state.current_user.first_name}', lambda: None)
                            ui.separator()
                            ui.menu_item('Settings', lambda: ui.open('/settings'))
                            ui.menu_item('Logout', handle_logout)
            else:
                ui.button('Sign In', on_click=lambda: create_auth_dialog().open()).classes('bg-white text-blue-700 hover:bg-gray-100')

def handle_logout():
    """Handle user logout."""
    state.logout()
    ui.notify('Logged out successfully', type='info')
    ui.open('/')

# Profile components
def create_profile_card(user: User, is_own_profile: bool = False):
    """Create user profile card."""
    with ui.card().classes('w-full p-6 mb-4'):
        with ui.row().classes('w-full items-start'):
            # Profile image placeholder
            with ui.column().classes('items-center mr-6'):
                ui.icon('account_circle', size='6rem').classes('text-gray-400')
                if is_own_profile:
                    ui.button('Edit Photo', icon='camera_alt', size='sm').classes('mt-2').props('outlined')
            
            # Profile information
            with ui.column().classes('flex-1'):
                ui.label(user.full_name).classes('text-2xl font-bold')
                if user.headline:
                    ui.label(user.headline).classes('text-lg text-gray-600 mb-2')
                if user.location:
                    ui.label(user.location).classes('text-sm text-gray-500 flex items-center')
                
                if user.summary:
                    ui.label('About').classes('text-lg font-semibold mt-4 mb-2')
                    ui.label(user.summary).classes('text-gray-700')
                
                if is_own_profile:
                    ui.button('Edit Profile', icon='edit', on_click=lambda: create_edit_profile_dialog().open()).classes('mt-4 bg-blue-600 text-white')

def create_edit_profile_dialog():
    """Create edit profile dialog."""
    with ui.dialog() as edit_dialog, ui.card().classes('w-96 p-6'):
        ui.label('Edit Profile').classes('text-xl font-bold mb-4')
        
        # Pre-fill with current user data
        user = state.current_user
        first_name_input = ui.input('First Name', value=user.first_name).classes('w-full mb-2')
        last_name_input = ui.input('Last Name', value=user.last_name).classes('w-full mb-2')
        headline_input = ui.input('Headline', value=user.headline or '').classes('w-full mb-2')
        location_input = ui.input('Location', value=user.location or '').classes('w-full mb-2')
        summary_input = ui.textarea('Summary', value=user.summary or '').classes('w-full mb-4')
        
        async def save_profile():
            try:
                user_update = UserUpdate(
                    first_name=first_name_input.value,
                    last_name=last_name_input.value,
                    headline=headline_input.value,
                    location=location_input.value,
                    summary=summary_input.value
                )
                
                updated_user = state.user_service.update_user(user.id, user_update)
                if updated_user:
                    state.current_user = updated_user
                    edit_dialog.close()
                    ui.notify('Profile updated successfully', type='positive')
                    ui.open('/profile')  # Refresh page
                else:
                    ui.notify('Failed to update profile', type='negative')
            except Exception as e:
                logger.error(f"Profile update error: {e}")
                ui.notify('Update failed', type='negative')
        
        with ui.row().classes('w-full justify-end space-x-2'):
            ui.button('Cancel', on_click=edit_dialog.close).props('outlined')
            ui.button('Save', on_click=save_profile).classes('bg-blue-600 text-white')
    
    return edit_dialog

def create_experience_section(user: User, is_own_profile: bool = False):
    """Create experience section."""
    with ui.card().classes('w-full p-6 mb-4'):
        with ui.row().classes('w-full items-center justify-between mb-4'):
            ui.label('Experience').classes('text-xl font-bold')
            if is_own_profile:
                ui.button('Add Experience', icon='add', on_click=lambda: create_add_experience_dialog().open()).props('outlined')
        
        # Get user experiences
        experiences = state.profile_service.get_user_experiences(user.id) if state.profile_service else []
        
        if experiences:
            for exp in experiences:
                with ui.row().classes('w-full items-start mb-4 pb-4 border-b border-gray-200'):
                    ui.icon('work', size='2rem').classes('text-gray-400 mr-4 mt-1')
                    with ui.column().classes('flex-1'):
                        ui.label(exp.title).classes('font-semibold text-lg')
                        ui.label(exp.company).classes('text-gray-600')
                        if exp.location:
                            ui.label(exp.location).classes('text-sm text-gray-500')
                        
                        date_range = f"{format_date(exp.start_date)} - {'Present' if exp.is_current else format_date(exp.end_date)}"
                        ui.label(date_range).classes('text-sm text-gray-500 mt-1')
                        
                        if exp.description:
                            ui.label(exp.description).classes('text-gray-700 mt-2')
        else:
            ui.label('No experience added yet').classes('text-gray-500 italic')

def create_add_experience_dialog():
    """Create add experience dialog."""
    with ui.dialog() as exp_dialog, ui.card().classes('w-96 p-6'):
        ui.label('Add Experience').classes('text-xl font-bold mb-4')
        
        title_input = ui.input('Job Title', placeholder='e.g. Software Engineer').classes('w-full mb-2')
        company_input = ui.input('Company', placeholder='e.g. Google').classes('w-full mb-2')
        location_input = ui.input('Location', placeholder='e.g. San Francisco, CA').classes('w-full mb-2')
        start_date_input = ui.input('Start Date', placeholder='YYYY-MM-DD').classes('w-full mb-2')
        end_date_input = ui.input('End Date', placeholder='YYYY-MM-DD (leave empty if current)').classes('w-full mb-2')
        is_current_checkbox = ui.checkbox('I currently work here').classes('mb-2')
        description_input = ui.textarea('Description', placeholder='Describe your role and achievements').classes('w-full mb-4')
        
        async def save_experience():
            try:
                from datetime import datetime
                
                start_date = datetime.strptime(start_date_input.value, '%Y-%m-%d').date()
                end_date = None
                if end_date_input.value and not is_current_checkbox.value:
                    end_date = datetime.strptime(end_date_input.value, '%Y-%m-%d').date()
                
                exp_create = ExperienceCreate(
                    title=title_input.value,
                    company=company_input.value,
                    location=location_input.value,
                    description=description_input.value,
                    start_date=start_date,
                    end_date=end_date,
                    is_current=is_current_checkbox.value
                )
                
                experience = state.profile_service.add_experience(state.current_user.id, exp_create)
                if experience:
                    exp_dialog.close()
                    ui.notify('Experience added successfully', type='positive')
                    ui.open('/profile')  # Refresh page
                else:
                    ui.notify('Failed to add experience', type='negative')
            except Exception as e:
                logger.error(f"Add experience error: {e}")
                ui.notify('Failed to add experience', type='negative')
        
        with ui.row().classes('w-full justify-end space-x-2'):
            ui.button('Cancel', on_click=exp_dialog.close).props('outlined')
            ui.button('Save', on_click=save_experience).classes('bg-blue-600 text-white')
    
    return exp_dialog

# Post components
def create_post_composer():
    """Create post composer."""
    with ui.card().classes('w-full p-4 mb-4'):
        ui.label('Share an update').classes('text-lg font-semibold mb-3')
        
        post_content = ui.textarea('What\'s on your mind?', placeholder='Share your thoughts with your network...').classes('w-full mb-3')
        
        async def create_post():
            try:
                if not post_content.value.strip():
                    ui.notify('Please enter some content', type='warning')
                    return
                
                post_create = PostCreate(content=post_content.value.strip())
                post = state.social_service.create_post(state.current_user.id, post_create)
                
                if post:
                    post_content.value = ''
                    ui.notify('Post shared successfully', type='positive')
                    ui.open('/dashboard')  # Refresh feed
                else:
                    ui.notify('Failed to create post', type='negative')
            except Exception as e:
                logger.error(f"Create post error: {e}")
                ui.notify('Failed to create post', type='negative')
        
        with ui.row().classes('w-full justify-between items-center'):
            with ui.row().classes('space-x-2'):
                ui.button('Photo', icon='photo', size='sm').props('outlined disabled')
                ui.button('Video', icon='videocam', size='sm').props('outlined disabled')
                ui.button('Document', icon='description', size='sm').props('outlined disabled')
            
            ui.button('Post', on_click=create_post).classes('bg-blue-600 text-white')

def create_post_card(post: Post):
    """Create post card."""
    with ui.card().classes('w-full p-4 mb-4'):
        # Post header
        with ui.row().classes('w-full items-center mb-3'):
            ui.icon('account_circle', size='2.5rem').classes('text-gray-400 mr-3')
            with ui.column().classes('flex-1'):
                ui.label(post.author.full_name).classes('font-semibold')
                ui.label(post.author.headline or 'Professional').classes('text-sm text-gray-600')
                ui.label(time_ago(post.created_at)).classes('text-xs text-gray-500')
        
        # Post content
        ui.label(post.content).classes('text-gray-800 mb-3')
        
        # Post stats
        if post.like_count > 0 or post.comment_count > 0:
            with ui.row().classes('w-full items-center justify-between text-sm text-gray-500 mb-3 pb-2 border-b border-gray-200'):
                if post.like_count > 0:
                    ui.label(f'{post.like_count} likes')
                if post.comment_count > 0:
                    ui.label(f'{post.comment_count} comments')
        
        # Post actions
        with ui.row().classes('w-full justify-around'):
            async def toggle_like():
                try:
                    state.social_service.like_post(state.current_user.id, post.id)
                    ui.open('/dashboard')  # Refresh to show updated likes
                except Exception as e:
                    logger.error(f"Like post error: {e}")
                    ui.notify('Failed to like post', type='negative')
            
            ui.button('Like', icon='thumb_up', on_click=toggle_like).classes('text-gray-600 hover:text-blue-600').props('flat')
            ui.button('Comment', icon='comment', on_click=lambda: create_comment_dialog(post).open()).classes('text-gray-600 hover:text-blue-600').props('flat')
            ui.button('Share', icon='share', on_click=lambda: ui.notify('Share feature coming soon')).classes('text-gray-600 hover:text-blue-600').props('flat')

def create_comment_dialog(post: Post):
    """Create comment dialog."""
    with ui.dialog() as comment_dialog, ui.card().classes('w-96 p-6'):
        ui.label(f'Comment on {post.author.first_name}\'s post').classes('text-lg font-bold mb-4')
        
        # Show original post content
        with ui.card().classes('w-full p-3 mb-4 bg-gray-50'):
            ui.label(post.content[:100] + ('...' if len(post.content) > 100 else '')).classes('text-sm text-gray-700')
        
        comment_input = ui.textarea('Write a comment...', placeholder='Share your thoughts...').classes('w-full mb-4')
        
        async def add_comment():
            try:
                if not comment_input.value.strip():
                    ui.notify('Please enter a comment', type='warning')
                    return
                
                comment_create = CommentCreate(content=comment_input.value.strip())
                comment = state.social_service.comment_on_post(state.current_user.id, post.id, comment_create)
                
                if comment:
                    comment_dialog.close()
                    ui.notify('Comment added successfully', type='positive')
                    ui.open('/dashboard')  # Refresh feed
                else:
                    ui.notify('Failed to add comment', type='negative')
            except Exception as e:
                logger.error(f"Add comment error: {e}")
                ui.notify('Failed to add comment', type='negative')
        
        with ui.row().classes('w-full justify-end space-x-2'):
            ui.button('Cancel', on_click=comment_dialog.close).props('outlined')
            ui.button('Comment', on_click=add_comment).classes('bg-blue-600 text-white')
    
    return comment_dialog

# Page definitions
@ui.page('/')
def landing_page():
    """Landing page."""
    create_navbar()
    
    with ui.column().classes('w-full max-w-4xl mx-auto p-8'):
        # Hero section
        with ui.row().classes('w-full items-center justify-between mb-12'):
            with ui.column().classes('flex-1 mr-8'):
                ui.label('Welcome to the professional community').classes('text-4xl font-bold mb-4')
                ui.label('Connect with professionals, share insights, and grow your career.').classes('text-xl text-gray-600 mb-6')
                
                if not state.current_user:
                    ui.button('Join now', on_click=lambda: create_auth_dialog().open()).classes('bg-blue-600 text-white text-lg px-8 py-3')
                else:
                    ui.button('Go to Dashboard', on_click=lambda: ui.open('/dashboard')).classes('bg-blue-600 text-white text-lg px-8 py-3')
            
            with ui.column().classes('items-center'):
                ui.icon('business', size='12rem').classes('text-blue-600')
        
        # Features section
        ui.label('Why join LinkedIn Clone?').classes('text-2xl font-bold mb-8 text-center')
        
        with ui.row().classes('w-full justify-around'):
            with ui.card().classes('w-64 p-6 text-center'):
                ui.icon('people', size='3rem').classes('text-blue-600 mb-4')
                ui.label('Connect').classes('text-xl font-semibold mb-2')
                ui.label('Build your professional network').classes('text-gray-600')
            
            with ui.card().classes('w-64 p-6 text-center'):
                ui.icon('trending_up', size='3rem').classes('text-green-600 mb-4')
                ui.label('Grow').classes('text-xl font-semibold mb-2')
                ui.label('Advance your career').classes('text-gray-600')
            
            with ui.card().classes('w-64 p-6 text-center'):
                ui.icon('lightbulb', size='3rem').classes('text-yellow-600 mb-4')
                ui.label('Learn').classes('text-xl font-semibold mb-2')
                ui.label('Share knowledge and insights').classes('text-gray-600')

@ui.page('/dashboard')
def dashboard_page():
    """Main dashboard/feed page."""
    if not state.current_user:
        ui.open('/')
        return
    
    if not state.social_service:
        state.initialize_services()
    
    create_navbar()
    
    with ui.row().classes('w-full max-w-6xl mx-auto p-4'):
        # Left sidebar - User info
        with ui.column().classes('w-64 mr-4'):
            create_profile_card(state.current_user, is_own_profile=True)
            
            # Quick stats
            with ui.card().classes('w-full p-4'):
                ui.label('Your Network').classes('font-semibold mb-2')
                connections = state.social_service.get_user_connections(state.current_user.id)
                ui.label(f'{len(connections)} connections').classes('text-sm text-gray-600')
                ui.button('Grow your network', on_click=lambda: ui.open('/network')).classes('mt-2 w-full').props('outlined')
        
        # Main feed
        with ui.column().classes('flex-1'):
            create_post_composer()
            
            # Feed posts
            posts = state.social_service.get_feed(state.current_user.id)
            
            if posts:
                for post in posts:
                    create_post_card(post)
            else:
                with ui.card().classes('w-full p-8 text-center'):
                    ui.icon('rss_feed', size='3rem').classes('text-gray-400 mb-4')
                    ui.label('Your feed is empty').classes('text-xl font-semibold mb-2')
                    ui.label('Connect with professionals to see their updates').classes('text-gray-600 mb-4')
                    ui.button('Find people to connect', on_click=lambda: ui.open('/network')).classes('bg-blue-600 text-white')

@ui.page('/profile')
def profile_page():
    """User profile page."""
    if not state.current_user:
        ui.open('/')
        return
    
    if not state.profile_service:
        state.initialize_services()
    
    create_navbar()
    
    with ui.column().classes('w-full max-w-4xl mx-auto p-4'):
        create_profile_card(state.current_user, is_own_profile=True)
        create_experience_section(state.current_user, is_own_profile=True)
        
        # Education section
        with ui.card().classes('w-full p-6 mb-4'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Education').classes('text-xl font-bold')
                ui.button('Add Education', icon='add', on_click=lambda: ui.notify('Add education feature coming soon')).props('outlined')
            
            education_list = state.profile_service.get_user_education(state.current_user.id)
            if education_list:
                for edu in education_list:
                    with ui.row().classes('w-full items-start mb-4'):
                        ui.icon('school', size='2rem').classes('text-gray-400 mr-4 mt-1')
                        with ui.column().classes('flex-1'):
                            ui.label(edu.school).classes('font-semibold text-lg')
                            if edu.degree:
                                ui.label(f'{edu.degree} in {edu.field_of_study}').classes('text-gray-600')
                            date_range = f"{format_date(edu.start_date)} - {format_date(edu.end_date)}"
                            ui.label(date_range).classes('text-sm text-gray-500')
            else:
                ui.label('No education added yet').classes('text-gray-500 italic')
        
        # Skills section
        with ui.card().classes('w-full p-6 mb-4'):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Skills').classes('text-xl font-bold')
                ui.button('Add Skill', icon='add', on_click=lambda: ui.notify('Add skill feature coming soon')).props('outlined')
            
            skills = state.profile_service.get_user_skills(state.current_user.id)
            if skills:
                with ui.row().classes('w-full flex-wrap'):
                    for skill in skills:
                        ui.chip(skill.name, icon='star' if skill.endorsements > 0 else None).classes('m-1')
            else:
                ui.label('No skills added yet').classes('text-gray-500 italic')

@ui.page('/network')
def network_page():
    """Network/connections page."""
    if not state.current_user:
        ui.open('/')
        return
    
    if not state.social_service:
        state.initialize_services()
    
    create_navbar()
    
    with ui.column().classes('w-full max-w-4xl mx-auto p-4'):
        ui.label('My Network').classes('text-2xl font-bold mb-6')
        
        # Pending requests
        pending_requests = state.social_service.get_pending_requests(state.current_user.id)
        if pending_requests:
            with ui.card().classes('w-full p-6 mb-6'):
                ui.label(f'Pending Requests ({len(pending_requests)})').classes('text-xl font-bold mb-4')
                
                for request in pending_requests:
                    with ui.row().classes('w-full items-center justify-between mb-4 pb-4 border-b border-gray-200'):
                        with ui.row().classes('items-center'):
                            ui.icon('account_circle', size='3rem').classes('text-gray-400 mr-4')
                            with ui.column():
                                ui.label(request.requester.full_name).classes('font-semibold')
                                ui.label(request.requester.headline or 'Professional').classes('text-sm text-gray-600')
                                if request.message:
                                    ui.label(f'"{request.message}"').classes('text-sm text-gray-700 italic mt-1')
                        
                        with ui.row().classes('space-x-2'):
                            async def accept_request(req_id=request.id):
                                try:
                                    state.social_service.respond_to_connection(req_id, state.current_user.id, True)
                                    ui.notify('Connection accepted', type='positive')
                                    ui.open('/network')  # Refresh
                                except Exception as e:
                                    logger.error(f"Accept connection error: {e}")
                                    ui.notify('Failed to accept connection', type='negative')
                            
                            async def decline_request(req_id=request.id):
                                try:
                                    state.social_service.respond_to_connection(req_id, state.current_user.id, False)
                                    ui.notify('Connection declined', type='info')
                                    ui.open('/network')  # Refresh
                                except Exception as e:
                                    logger.error(f"Decline connection error: {e}")
                                    ui.notify('Failed to decline connection', type='negative')
                            
                            ui.button('Accept', on_click=accept_request).classes('bg-blue-600 text-white')
                            ui.button('Decline', on_click=decline_request).props('outlined')
        
        # Current connections
        connections = state.social_service.get_user_connections(state.current_user.id)
        
        with ui.card().classes('w-full p-6 mb-6'):
            ui.label(f'Your Connections ({len(connections)})').classes('text-xl font-bold mb-4')
            
            if connections:
                for connection in connections:
                    # Determine the other user in the connection
                    other_user = connection.addressee if connection.requester_id == state.current_user.id else connection.requester
                    
                    with ui.row().classes('w-full items-center mb-4 pb-4 border-b border-gray-200'):
                        ui.icon('account_circle', size='3rem').classes('text-gray-400 mr-4')
                        with ui.column().classes('flex-1'):
                            ui.label(other_user.full_name).classes('font-semibold')
                            ui.label(other_user.headline or 'Professional').classes('text-sm text-gray-600')
                            ui.label(f'Connected on {connection.created_at.strftime("%B %d, %Y")}').classes('text-xs text-gray-500')
                        
                        ui.button('Message', icon='message').props('outlined disabled')
            else:
                ui.label('No connections yet. Start building your network!').classes('text-gray-500 italic')
        
        # People you may know
        with ui.card().classes('w-full p-6'):
            ui.label('People you may know').classes('text-xl font-bold mb-4')
            
            # Get all users except current user and existing connections
            all_users = state.user_service.get_all_users(limit=10)
            connected_user_ids = set()
            
            for conn in connections:
                if conn.requester_id == state.current_user.id:
                    connected_user_ids.add(conn.addressee_id)
                else:
                    connected_user_ids.add(conn.requester_id)
            
            # Filter out current user and existing connections
            suggested_users = [user for user in all_users 
                             if user.id != state.current_user.id and user.id not in connected_user_ids]
            
            if suggested_users:
                for user in suggested_users[:5]:  # Show max 5 suggestions
                    with ui.row().classes('w-full items-center justify-between mb-4 pb-4 border-b border-gray-200'):
                        with ui.row().classes('items-center'):
                            ui.icon('account_circle', size='3rem').classes('text-gray-400 mr-4')
                            with ui.column():
                                ui.label(user.full_name).classes('font-semibold')
                                ui.label(user.headline or 'Professional').classes('text-sm text-gray-600')
                        
                        async def send_connection_request(user_id=user.id):
                            try:
                                connection_create = ConnectionCreate(addressee_id=user_id)
                                connection = state.social_service.send_connection_request(state.current_user.id, connection_create)
                                
                                if connection:
                                    ui.notify('Connection request sent', type='positive')
                                    ui.open('/network')  # Refresh
                                else:
                                    ui.notify('Failed to send connection request', type='negative')
                            except Exception as e:
                                logger.error(f"Send connection error: {e}")
                                ui.notify('Failed to send connection request', type='negative')
                        
                        ui.button('Connect', on_click=send_connection_request).classes('bg-blue-600 text-white')
            else:
                ui.label('No new people to suggest at the moment.').classes('text-gray-500 italic')

# Initialize services when the app starts
state.initialize_services()

# Set up the app
ui.run_with(app, title='LinkedIn Clone', favicon='🔗')