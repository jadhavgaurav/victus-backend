# Figma Make AI Prompt: Advanced AI Assistant UI (Next.js)

## Project Overview
Create a complete, production-ready Next.js web application for an AI assistant interface inspired by ChatGPT, Jarvis, and modern AI chatbot platforms. This is a full-stack frontend that will connect to a FastAPI backend API. The application must be fully functional, responsive, and follow Next.js best practices.

## Design Inspiration References
**CRITICAL**: Review these design inspirations before starting:
- **Liquid Glass UI**: [Dribbble - Liquid Glass Modal](https://dribbble.com/shots/26536796-Liquid-Glass-UI-Modal-Window) - Advanced glass morphism with liquid effects
- **OKAI AI Chatbot**: [Dribbble - OKAI AI Platform](https://dribbble.com/shots/24964124-OKAI-AI-Online-AI-Chatbot-Platform) - Modern AI chatbot interface patterns
- **Omni Agent Dashboard**: [Dribbble - Omni Agent](https://dribbble.com/shots/26427853-Omni-Agent-Smart-AI-Copilot-Assistant-Dashboard-UI-UX-Design) - Smart AI copilot dashboard design
- **Chatbot Concepts**: [Pinterest - Chatbot Design](https://in.pinterest.com/pin/844493671298625/) - Modern chatbot UI patterns
- **App Interface Design**: [Pinterest - App Design](https://in.pinterest.com/pin/1618549864633295/) - Purple-themed app interfaces

**Key Design Elements to Extract**:
- Liquid glass effects with advanced blur and transparency
- Smooth, flowing animations
- Modern AI chatbot conversation flows
- Dashboard-style information architecture
- Premium glass morphism throughout
- Sophisticated color gradients
- Clean, minimal interface with maximum functionality

## Backend API Integration
The frontend will connect to a FastAPI backend with the following endpoints:
- `POST /api/chat` - Server-Sent Events (SSE) streaming chat endpoint
- `POST /api/history` - Get chat history for a session
- `POST /api/auth/login` - User authentication
- `POST /api/auth/signup` - User registration
- `GET /api/auth/me` - Get current user profile
- `POST /api/transcribe` - Voice transcription
- `POST /api/synthesize` - Text-to-speech synthesis
- `POST /api/upload` - Document upload for RAG

**API Base URL**: Should be configurable via environment variable `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`)

**SSE Event Format**:
- `EVENT_TOOL_START:{tool_name}|{tool_input}` - Tool execution started
- `EVENT_TOOL_END:{tool_name}` - Tool execution completed
- `OUTPUT_STREAM:{chunk}` - AI response chunk
- `STREAM_END` - Stream completed
- `ERROR:{error_message}` - Error occurred

## Design Requirements

### Typography
- **Primary Font**: DM Sans (Google Fonts)
  - Import: `@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');`
  - Font family: `'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
  - Base font size: `16px` (1rem)
  - Line height: `1.5` for body text, `1.4` for headings
  - Font weights:
    - Regular: 400 (body text)
    - Medium: 500 (labels, buttons)
    - Semi-bold: 600 (headings, emphasis)
    - Bold: 700 (strong emphasis)

### Color Scheme
- **Primary Gradient**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
  - Use for: User chat bubbles, primary buttons, active states, headers
  - Start color: #667eea (Soft purple-blue)
  - End color: #764ba2 (Deep purple)
  
- **Background Colors**:
  - Main background: Dark theme with gradient overlay
    - Base: `#0F172A` or `#1E293B` (Dark slate)
    - Alternative: Light gradient background `#f8f9fa` for chat area (if light mode)
  - Glass morphism backgrounds: `rgba(255, 255, 255, 0.05)` to `rgba(255, 255, 255, 0.15)`
  - Sidebar background: Dark with glass morphism effect
  - Chat area background: `#f8f9fa` (light gray) or dark equivalent
  
- **Chat Bubble Colors**:
  - **User Messages** (Right-aligned):
    - Background: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
    - Text color: `#FFFFFF` (Pure white for maximum contrast)
    - Border: None
    - Shadow: `0 2px 8px rgba(102, 126, 234, 0.3)`
  
  - **AI Messages** (Left-aligned):
    - Background: `#FFFFFF` (Pure white) or `rgba(255, 255, 255, 0.95)` for dark theme
    - Text color: `#333333` (Dark gray for excellent readability)
    - Border: `1px solid #e0e0e0` (Subtle border for definition)
    - Shadow: `0 1px 3px rgba(0, 0, 0, 0.1)`
  
- **Text Colors**:
  - Primary text: `#FFFFFF` (white) for dark backgrounds, `#333333` for light backgrounds
  - Secondary text: `#666666` (medium gray) or `#94A3B8` (slate gray)
  - Muted text: `#999999` (light gray)
  - Accent text: Purple-pink gradient for special emphasis
  
- **Border Colors**: 
  - Default: `#e0e0e0` (light gray)
  - Focus: `#667eea` (purple)
  - Glass morphism: `rgba(255, 255, 255, 0.1)`
  
- **State Colors**:
  - Error: `#EF4444` (Soft red)
  - Success: `#10B981` (Soft green)
  - Warning: `#F59E0B` (Amber)
  - Info: `#3B82F6` (Blue)

### Visual Style

#### Rounded Corners (CRITICAL - Apply Everywhere)
- **Chat Bubbles**: 
  - Base radius: `18px` (1.125rem)
  - User messages: `border-radius: 18px` with `border-bottom-right-radius: 4px` (chat bubble tail effect)
  - AI messages: `border-radius: 18px` with `border-bottom-left-radius: 4px` (chat bubble tail effect)
  
- **Buttons**: 
  - Primary buttons: `border-radius: 25px` (pill shape)
  - Secondary buttons: `border-radius: 12px`
  - Icon buttons: `border-radius: 50%` (circular) or `12px` (rounded square)
  
- **Cards & Panels**:
  - Main cards: `border-radius: 20px`
  - Sidebar items: `border-radius: 12px`
  - Input fields: `border-radius: 25px` (pill shape) or `10px` (rounded)
  - Dropdowns: `border-radius: 12px`
  - Modals/Drawers: `border-radius: 20px` (top corners)
  
- **Badges & Tags**: `border-radius: 12px` (pill shape)

#### Liquid Glass Morphism (Advanced)
- Apply throughout the UI for modern, premium feel inspired by liquid glass designs
- **Properties**:
  - Backdrop blur: `backdrop-blur-xl` (24px) or `backdrop-blur-2xl` (40px)
  - Background: `rgba(255, 255, 255, 0.05)` to `rgba(255, 255, 255, 0.15)`
  - **Advanced**: Use `rgba(255, 255, 255, 0.08)` with subtle gradient overlay for liquid effect
  - Border: `1px solid rgba(255, 255, 255, 0.2)` (slightly more visible for definition)
  - **Inner Glow**: `inset 0 1px 0 rgba(255, 255, 255, 0.1)` for depth
  - Border radius: `12px` to `20px` (matching rounded corner requirements)
  - Shadow: `0 8px 32px rgba(0, 0, 0, 0.15)` with colored tint `0 8px 32px rgba(102, 126, 234, 0.1)`
  - **Liquid Effect**: Subtle gradient overlay from top-left to bottom-right
  - **Reflection**: Optional subtle highlight on top edge for glass-like appearance

#### Gradients
- **Primary Gradient**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
  - Use for: User chat bubbles, primary buttons, active states, headers
- **Hover Gradients**: Slightly lighter version of primary gradient
- **Text Gradients**: Apply to headings and special text elements
- **Background Gradients**: Subtle gradients for depth

#### Shadows
- **Elevation Levels**:
  - Level 1 (subtle): `0 1px 3px rgba(0, 0, 0, 0.1)`
  - Level 2 (cards): `0 4px 12px rgba(0, 0, 0, 0.15)`
  - Level 3 (modals): `0 20px 60px rgba(0, 0, 0, 0.3)`
  - Colored shadows: `0 4px 12px rgba(102, 126, 234, 0.4)` for purple elements

#### Spacing & Layout
- **Padding**:
  - Chat bubbles: `12px 18px` (vertical horizontal)
  - Buttons: `12px 20px` (pill buttons), `10px 16px` (regular buttons)
  - Input fields: `15px 20px`
  - Cards: `20px` to `30px`
  
- **Gaps**:
  - Between messages: `20px`
  - Between buttons: `8px` to `10px`
  - Between form elements: `20px`
  
- **Margins**:
  - Section spacing: `24px` to `32px`
  - Element spacing: `12px` to `16px`

#### Visibility & Contrast
- **Text Contrast**: 
  - Minimum contrast ratio: 4.5:1 for normal text, 3:1 for large text (WCAG AA)
  - White text on gradient: Excellent contrast
  - Dark text on white: Excellent contrast
  - Avoid gray text on gray backgrounds
  
- **Clear Visual Hierarchy**:
  - Use font weights (400, 500, 600, 700) for hierarchy
  - Use size differences (16px base, 14px secondary, 12px small)
  - Use color intensity for emphasis
  - Use spacing for grouping
  
- **Focus States**:
  - All interactive elements must have visible focus indicators
  - Focus ring: `2px solid #667eea` with `outline-offset: 2px`
  - Focus background: Slight color change or glow effect

#### Animations & Transitions
- **Timing**: 
  - Fast: `150ms` (hover states)
  - Normal: `200ms` to `300ms` (most transitions)
  - Slow: `400ms` to `500ms` (page transitions)
  
- **Easing**:
  - Default: `ease-in-out`
  - Smooth: `cubic-bezier(0.4, 0, 0.2, 1)`
  - Bounce: `cubic-bezier(0.68, -0.55, 0.265, 1.55)` (for playful elements)
  
- **Animations**:
  - Message appearance: `fadeIn` with `translateY(10px)` to `translateY(0)`
  - Button hover: `scale(1.05)` or `translateY(-2px)`
  - Typing indicator: Animated dots with bounce
  - Tool execution: Pulse animation
  - Page transitions: Smooth fade/slide

#### Icons
- **Library**: Lucide React (preferred) or Heroicons
- **Size**: 
  - Small: `16px` (inline with text)
  - Medium: `20px` (buttons, navigation)
  - Large: `24px` (featured icons)
- **Style**: Outline style for consistency
- **Color**: Inherit text color or use accent colors

## Layout Structure

### Main Layout (Full Screen)
```
┌─────────────────────────────────────────────────────────┐
│  [Sidebar]  │           [Main Chat Area]                │
│             │                                            │
│  - Logo     │  ┌────────────────────────────────────┐  │
│  - New Chat │  │  Chat Messages (scrollable)         │  │
│  - History  │  │                                    │  │
│  - Settings │  │                                    │  │
│  - Model    │  │                                    │  │
│  - Profile  │  └────────────────────────────────────┘  │
│             │  [Input Area with send button]           │
└─────────────┴───────────────────────────────────────────┘
```

### Sidebar (Left Panel)
**Width**: 
- Desktop: 280px (fixed)
- Tablet: 260px
- Mobile: Slide-in drawer (280px width, overlay)

**Styling**:
- **Background**: Dark theme with **liquid glass morphism** effect
  - Base: Dark background with gradient overlay
  - Glass: `rgba(255, 255, 255, 0.08)` with `backdrop-blur-2xl`
  - Border: Right border `1px solid rgba(255, 255, 255, 0.15)` with subtle glow
  - **Liquid Effect**: Subtle gradient from top (lighter) to bottom (darker)
- **Border Radius**: `0` (full height) or `20px` on right side only
- **Padding**: `20px` (top/bottom), `16px` (left/right)
- **Font**: DM Sans throughout
- **Clear Separation**: Visual separation from main chat area with subtle divider
- **Scrollable**: Smooth scrolling with custom scrollbar styling (thin, glass-like)
- **Depth**: Multiple layers with subtle shadows for 3D effect

**Components**:
1. **Logo/Brand Section** (Top)
   - App name "VICTUS" with gradient text
   - Optional: Small animated icon/logo

2. **New Chat Button**
   - **Background**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
   - **Text Color**: `#FFFFFF` (white)
   - **Border Radius**: `12px` (rounded)
   - **Padding**: `12px 20px`
   - **Font**: DM Sans, 16px, weight 600
   - **Icon**: Plus icon (20px), left of text
   - **Hover**: `scale(1.02)`, `box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4)`
   - **Transition**: `all 0.3s ease-in-out`
   - Creates new session and clears current chat

3. **Chat History Section**
   - Scrollable list of previous conversations
   - **Search/Filter Bar** (at top of history)
     - Search input to filter conversations
     - Filter by date range
     - Filter by keywords
   - Each item shows:
     - Truncated first message or "New Chat" if empty
     - Timestamp (relative: "2 hours ago", "Yesterday", etc.)
     - Message count badge
     - Active state highlighting
     - Pin icon (pin important conversations to top)
   - **Styling**:
     - **Background**: Glass morphism or transparent
     - **Border Radius**: `12px` (rounded corners)
     - **Padding**: `12px 16px`
     - **Hover**: Background `rgba(102, 126, 234, 0.1)`, smooth transition
     - **Active State**: Purple gradient background or purple border
     - **Font**: DM Sans, 14px (title), 12px (timestamp)
     - **Clear Visibility**: High contrast text, readable at all sizes
   - **Actions on hover**:
     - Edit conversation title
     - Delete conversation (with confirmation)
     - Pin/Unpin conversation
     - Export conversation (JSON/PDF)
   - **Grouping**:
     - Today
     - Yesterday
     - This Week
     - This Month
     - Older
   - Click to load that conversation
   - Hover effects with glass morphism

4. **Model Selector Dropdown**
   - **Background**: Glass morphism or white/dark background
   - **Border**: `1px solid rgba(255, 255, 255, 0.1)` or `#e0e0e0`
   - **Border Radius**: `12px` (rounded)
   - **Padding**: `12px 16px`
   - **Font**: DM Sans, 14px, weight 500
   - **Label**: "Model" (12px, gray, above dropdown)
   - Dropdown with GPT models:
     - GPT-4o (default) - "Most capable"
     - GPT-4o-mini - "Fast & efficient"
     - GPT-4-turbo - "Balanced"
     - GPT-4 - "High quality"
     - GPT-3.5-turbo - "Fastest"
   - Display current selection with model description
   - **Dropdown Menu**: 
     - Border radius: `12px`
     - Shadow: `0 8px 32px rgba(0, 0, 0, 0.2)`
     - Each option: `12px` padding, hover state
   - Store selection in localStorage
   - Show model capabilities/limits
   - Icon: ChevronDown (16px, right-aligned)
   - Model status indicator (available/unavailable)
   - **Clear Visibility**: Readable text, clear selection state

5. **Quick Access Buttons** (Optional, collapsible section)
   - **Documents Button** (📄 icon)
     - Shows uploaded documents count
     - Click to open documents manager
   - **Email Quick Access** (✉️ icon)
     - Shows unread email count (if M365 connected)
     - Click to view recent emails
   - **Calendar Quick Access** (📅 icon)
     - Shows next event time
     - Click to view calendar
   - **Memory/Facts** (🧠 icon)
     - Shows stored facts count
     - Click to manage facts

6. **Settings Button**
   - Icon: Settings/Cog
   - Text: "Settings"
   - Opens settings panel/drawer
   - Badge indicator if settings need attention

7. **User Profile Section** (Bottom)
   - User avatar/initials (clickable)
   - Username/email
   - **Status Indicator**:
     - Online/Offline status
     - API connection status
   - **Quick Menu** (click avatar):
     - View Profile
     - Settings
     - Logout
   - Logout button (always visible)

### Main Chat Area
**Layout**:
- Full height minus input area
- Scrollable message container
- Auto-scroll to bottom on new messages
- **Background**: 
  - Light mode: `#f8f9fa` (light gray) or subtle gradient
  - Dark mode: Dark background with subtle gradient overlay
  - **Optional**: Subtle pattern or texture for depth (very subtle)
- **Padding**: `20px` to `24px` (generous spacing)
- **Message Spacing**: `20px` between messages (clear separation)

**Message Components**:
1. **User Messages** (Right-aligned)
   - **Background**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)` (purple gradient)
   - **Text Color**: `#FFFFFF` (pure white for maximum contrast)
   - **Border Radius**: `18px` with `border-bottom-right-radius: 4px` (chat bubble tail)
   - **Padding**: `12px 18px`
   - **Max Width**: `70%` of container
   - **Shadow**: `0 2px 8px rgba(102, 126, 234, 0.3)`
   - **Font**: DM Sans, 16px, weight 400
   - **Line Height**: 1.5
   - **Alignment**: Right-aligned with flex-end
   - **Avatar**: Optional user initials or icon (small, 32px circle)
   - **Animation**: Fade in with slight upward motion

2. **AI Messages** (Left-aligned)
   - **Background**: `#FFFFFF` (pure white) or `rgba(255, 255, 255, 0.95)` for dark theme
   - **Text Color**: `#333333` (dark gray for excellent readability)
   - **Border**: `1px solid #e0e0e0` (subtle border for definition)
   - **Border Radius**: `18px` with `border-bottom-left-radius: 4px` (chat bubble tail)
   - **Padding**: `12px 18px`
   - **Max Width**: `70%` of container
   - **Shadow**: `0 1px 3px rgba(0, 0, 0, 0.1)`
   - **Font**: DM Sans, 16px, weight 400
   - **Line Height**: 1.5
   - **Alignment**: Left-aligned
   - **Avatar**: AI icon (sparkle/robot icon, 32px circle, purple gradient background)
   - **Markdown Rendering**: Full support with proper styling
   - **Code Blocks**: 
     - Background: `#f4f4f4` or `#1e293b` (dark theme)
     - Border radius: `8px`
     - Padding: `12px 16px`
     - Syntax highlighting with copy button (top-right corner)
   - **Clear Visual Separation**: Each message clearly distinct with proper spacing
   - **Message Actions** (on hover):
     - Copy message button
     - Regenerate response button (re-send last user message)
     - Edit & resend (edit user message, resend)
     - Thumbs up/down feedback
     - Share conversation button
   - **Rich Content Support**:
     - Tables with proper formatting
     - Lists (ordered/unordered)
     - Links (clickable, open in new tab)
     - Images (if backend supports)
     - Email preview cards (if email content detected)
     - Calendar event previews (if event detected)

3. **Tool Execution Indicators**
   - Show when tool is executing
   - Format: "🔧 Using {tool_name}..." with icon
   - Loading spinner with progress (if available)
   - Expandable tool details (click to see input/output)
   - Color-coded by tool type:
     - Email: Blue
     - Calendar: Green
     - Weather: Yellow
     - Documents: Purple
     - System: Gray
   - Appears between user message and AI response

4. **Typing Indicator**
   - Animated dots when AI is responding
   - Purple/pink gradient dots

5. **Welcome Message** (First load)
   - Centered welcome card with glass morphism
   - App introduction with animated logo
   - **Example Prompts/Suggestions** (clickable cards):
     - "Check the weather in Mumbai"
     - "Read my latest emails"
     - "What's on my calendar today?"
     - "Search the web for..."
     - "Remember that..."
   - **Quick Stats** (if user has history):
     - Total conversations
     - Messages exchanged
     - Documents uploaded
     - Facts stored
   - **Getting Started Guide** (collapsible)
     - How to use voice input
     - How to upload documents
     - How to use integrations

### Input Area (Bottom)
**Styling**:
- **Background**: Liquid glass morphism or solid background
- **Border Top**: `1px solid rgba(255, 255, 255, 0.1)` (subtle divider)
- **Padding**: `20px` (generous spacing)
- **Elevation**: Slight shadow above for depth

**Components**:
1. **Text Input**
   - Multi-line textarea (auto-expands up to 4-5 lines)
   - **Placeholder**: "Message VICTUS..." or "Type your message..."
   - **Background**: `#FFFFFF` (white) or glass morphism for dark theme
   - **Border**: `2px solid #e0e0e0` (default), `2px solid #667eea` (focus)
   - **Border Radius**: `25px` (pill shape for modern look)
   - **Padding**: `15px 20px`
   - **Font**: DM Sans, 16px, weight 400
   - **Focus State**: 
     - Border color: `#667eea` (purple)
     - Box shadow: `0 0 0 3px rgba(102, 126, 234, 0.1)`
     - Smooth transition: `border-color 0.3s, box-shadow 0.3s`
   - **Character Counter**: Optional, small text (12px, gray) in bottom-right
   - **Clear Visibility**: High contrast text, readable placeholder

2. **Action Buttons** (Right side of input):
   - **Voice Input Button** (Microphone icon)
     - **Background**: `#f0f0f0` (light gray) or glass morphism
     - **Border Radius**: `25px` (pill shape) or `50%` (circular)
     - **Padding**: `12px 20px` or `12px` (circular)
     - **Size**: `44px` minimum (touch-friendly)
     - **Hover**: Background `#e0e0e0`, `scale(1.05)`
     - **Active/Recording**: Pulsing animation with purple gradient background
     - **Icon**: 20px, centered
     - **Transition**: `all 0.3s ease-in-out`
   
   - **Send Button** (Arrow/Send icon)
     - **Background**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
     - **Text Color**: `#FFFFFF` (white)
     - **Border Radius**: `25px` (pill shape)
     - **Padding**: `12px 20px`
     - **Font**: DM Sans, 16px, weight 600
     - **Disabled State**: 
       - Opacity: `0.5`
       - Cursor: `not-allowed`
       - No hover effects
     - **Hover**: `scale(1.05)`, `box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4)`
     - **Loading State**: Spinner icon, disabled state
     - **Clear Visibility**: High contrast, prominent placement

3. **Additional Options** (Collapsible menu):
   - **File Upload Button** (for documents - PDF, DOCX)
     - Drag & drop support
     - File preview before upload
     - Upload progress indicator
     - Show uploaded documents count
   - **Voice Output Toggle** (Play audio responses)
   - **Clear Chat Button** (with confirmation)
   - **Quick Actions Menu** (⚡ icon)
     - "Check Weather" - Quick weather query
     - "Read Emails" - Quick email check
     - "View Calendar" - Show upcoming events
     - "Search Web" - Open web search prompt

### Settings Panel/Drawer
**Trigger**: Click Settings button in sidebar
**Layout**: Slide-in from right (desktop) or full-screen overlay (mobile)

**Styling** (Inspired by Liquid Glass UI):
- **Background**: Liquid glass morphism with advanced blur
  - Base: Dark background with gradient
  - Glass: `rgba(255, 255, 255, 0.1)` with `backdrop-blur-2xl` (40px)
  - Border: `1px solid rgba(255, 255, 255, 0.2)` with inner glow
  - **Liquid Effect**: Flowing gradient overlay for depth
- **Border Radius**: `20px` (top-left, bottom-left for slide-in)
- **Shadow**: `0 20px 60px rgba(0, 0, 0, 0.3)` with purple tint
- **Animation**: Smooth slide-in with fade (300ms ease-out)
- **Content**: Clear, organized sections with proper spacing
- **Backdrop**: Semi-transparent overlay with blur (`backdrop-blur-sm`)

**Sections** (Tabbed or Accordion layout):
1. **Profile Section**
   - User avatar (editable, upload image)
   - Username display (editable)
   - Email display (read-only, show verification status)
   - Display name field
   - Timezone selector
   - Edit profile button
   - Save changes button

2. **Context/System Prompt Section**
   - Textarea for custom context
   - Label: "System Context"
   - Placeholder: "Add custom context that will be included in every conversation..."
   - Save button
   - Character limit: 2000 characters with counter
   - Info tooltip explaining usage
   - Preset templates (Developer, Writer, Student, etc.)
   - Clear context button

3. **Integrations Section**
   - **Microsoft 365 Connection**
     - Connect/Disconnect button
     - Connection status indicator
     - Last sync time
     - Permissions granted list
   - **API Keys Management** (if user can add custom keys)
     - Web search API key
     - Weather API key
     - Other integrations

4. **Documents Management**
   - List of uploaded documents
   - Document name, upload date, status
   - Delete document button
   - Re-index document button
   - Upload new document button
   - Document count and storage usage

5. **Memory/Facts Management**
   - List of stored facts (key-value pairs)
   - Search facts
   - Add new fact button
   - Edit fact button
   - Delete fact button (with confirmation)
   - Export facts (JSON)
   - Import facts (JSON)
   - Facts count display

6. **Preferences Section**
   - **Appearance**:
     - Theme toggle (Dark/Light - if light theme supported)
     - Font size selector (Small/Medium/Large)
     - Compact/Comfortable spacing toggle
   - **Chat Behavior**:
     - Voice output toggle
     - Auto-scroll toggle
     - Markdown rendering toggle
     - Code syntax highlighting toggle
   - **Notifications**:
     - Email notifications toggle
     - Sound notifications toggle
     - Desktop notifications toggle
   - **Privacy**:
     - Clear chat history option
     - Clear all data option
     - Data export option

7. **Keyboard Shortcuts Section**
   - List of all keyboard shortcuts
   - Search shortcuts
   - Customizable shortcuts (if supported)
   - Visual keyboard layout

8. **About Section**
   - App version
   - API status indicator (real-time)
   - Backend health check
   - System information
   - Links to documentation
   - Release notes/changelog
   - Feedback button

9. **Account Actions**
   - Export all data (JSON/PDF)
   - Logout button
   - Delete account (with confirmation and password verification)

## Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Adaptations
- Sidebar becomes slide-in drawer with overlay
- Settings panel becomes full-screen modal
- Input area fixed at bottom
- Messages optimized for smaller screens
- Touch-friendly button sizes (min 44x44px)

### Tablet Adaptations
- Sidebar can be collapsible
- Optimized spacing and typography

### Desktop Enhancements
- Full sidebar always visible
- Larger chat area
- **Command Palette** (`Cmd/Ctrl + K`):
  - Quick search conversations
  - Quick actions (New chat, Settings, etc.)
  - Command shortcuts
  - Fuzzy search support
- **Keyboard Shortcuts**:
  - `Cmd/Ctrl + K`: Open command palette
  - `Cmd/Ctrl + N`: New chat
  - `Cmd/Ctrl + /`: Show keyboard shortcuts
  - `Cmd/Ctrl + ,`: Open settings
  - `Esc`: Close modals/drawers
  - `Cmd/Ctrl + Enter`: Send message (if multiline)
  - `Enter`: Send message (single line)
  - `Shift + Enter`: New line in input
  - `Cmd/Ctrl + F`: Search in current conversation
  - `Cmd/Ctrl + S`: Export current conversation

## Progressive Web App (PWA) Requirements

### Manifest Configuration
- App name: "VICTUS AI Assistant"
- Short name: "VICTUS"
- Description: "Advanced AI Assistant powered by GPT"
- Theme color: Primary purple (#6B46C1)
- Background color: Dark background color
- Display: "standalone"
- Icons: Multiple sizes (192x192, 512x512, etc.)
- Start URL: "/"
- Orientation: "portrait-primary"

### Service Worker
- Cache static assets
- Offline fallback page
- Cache API responses (with expiration)
- Background sync for failed requests

### PWA Features
- Install prompt
- Offline indicator
- Update notification
- Push notifications (optional, for future)

## Technical Requirements

### Next.js Setup
- **Framework**: Next.js 14+ (App Router)
- **TypeScript**: Full TypeScript implementation
- **Styling**: Tailwind CSS with custom configuration
  - **Font Import**: Add DM Sans from Google Fonts in `layout.tsx` or `globals.css`
  - **Custom Tailwind Config**: 
    - Extend theme with custom colors matching the design system
    - Custom border radius values (12px, 18px, 20px, 25px)
    - Custom shadows matching elevation levels
    - Custom gradients for purple theme
- **State Management**: React Context API or Zustand (for chat state, settings)
- **HTTP Client**: Native fetch with SSE support for streaming
- **Markdown**: `react-markdown` with syntax highlighting (`react-syntax-highlighter`)
- **Icons**: `lucide-react` (preferred) or `@heroicons/react`
- **Date Formatting**: `date-fns` for relative timestamps
- **Form Handling**: React Hook Form (for settings, login)
- **Audio**: Web Audio API for voice input/output
- **Command Palette**: `cmdk` or custom implementation
- **File Upload**: `react-dropzone` for drag & drop
- **PDF Export**: `jspdf` and `html2canvas` for PDF generation
- **Charts**: `recharts` or `chart.js` for usage statistics
- **Toast Notifications**: `sonner` or `react-hot-toast`
- **Fuzzy Search**: `fuse.js` for command palette and search

### Typography Setup
- **Font Import** (in `app/layout.tsx` or `globals.css`):
  ```css
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
  ```
- **Tailwind Config** (add to `tailwind.config.js`):
  ```js
  fontFamily: {
    sans: ['DM Sans', 'system-ui', 'sans-serif'],
  }
  ```
- **Global Styles**: Set base font to DM Sans in `globals.css`

### Project Structure
```
project-victus-frontend/
├── app/
│   ├── layout.tsx                 # Root layout with providers
│   ├── page.tsx                    # Main chat page
│   ├── login/
│   │   └── page.tsx                # Login page
│   ├── signup/
│   │   └── page.tsx                # Signup page
│   └── api/                        # API route handlers (if needed)
│       └── proxy/
│           └── route.ts            # API proxy (optional)
├── components/
│   ├── chat/
│   │   ├── ChatMessage.tsx         # Individual message component
│   │   ├── ChatInput.tsx           # Input area component
│   │   ├── ChatContainer.tsx       # Messages container
│   │   ├── TypingIndicator.tsx    # Loading dots animation
│   │   ├── ToolIndicator.tsx      # Tool execution indicator
│   │   ├── MessageActions.tsx      # Message action buttons
│   │   ├── WelcomeCard.tsx         # Welcome message component
│   │   └── QuickPrompts.tsx        # Example prompts component
│   ├── sidebar/
│   │   ├── Sidebar.tsx             # Main sidebar component
│   │   ├── ChatHistory.tsx         # History list component
│   │   ├── ChatHistoryItem.tsx     # Single history item
│   │   ├── ChatHistorySearch.tsx   # History search/filter
│   │   ├── ModelSelector.tsx       # Model dropdown
│   │   ├── UserProfile.tsx         # Profile section
│   │   ├── QuickActions.tsx        # Quick access buttons
│   │   └── DocumentsButton.tsx     # Documents quick access
│   ├── settings/
│   │   ├── SettingsPanel.tsx       # Main settings panel
│   │   ├── ProfileSection.tsx      # Profile settings
│   │   ├── ContextSection.tsx      # Context input
│   │   ├── PreferencesSection.tsx  # User preferences
│   │   ├── IntegrationsSection.tsx # M365 and API integrations
│   │   ├── DocumentsSection.tsx    # Documents management
│   │   ├── MemorySection.tsx       # Facts/memory management
│   │   ├── ShortcutsSection.tsx    # Keyboard shortcuts
│   │   └── AboutSection.tsx        # About and info
│   ├── panels/
│   │   ├── DocumentsPanel.tsx      # Documents manager panel
│   │   ├── EmailPanel.tsx          # Email quick view panel
│   │   ├── CalendarPanel.tsx       # Calendar quick view panel
│   │   ├── MemoryPanel.tsx         # Memory/facts panel
│   │   └── NotificationsPanel.tsx  # Notifications center
│   ├── command-palette/
│   │   ├── CommandPalette.tsx      # Main command palette
│   │   ├── CommandItem.tsx         # Command item component
│   │   └── CommandSearch.tsx       # Command search input
│   ├── ui/
│   │   ├── Button.tsx              # Reusable button component
│   │   ├── Input.tsx               # Reusable input component
│   │   ├── Dropdown.tsx            # Dropdown component
│   │   ├── Modal.tsx               # Modal component
│   │   ├── Drawer.tsx              # Drawer component
│   │   └── GlassCard.tsx           # Glass morphism card
│   └── layout/
│       ├── Header.tsx               # Top header (if needed)
│       └── MainLayout.tsx           # Main layout wrapper
├── lib/
│   ├── api/
│   │   ├── client.ts               # API client configuration
│   │   ├── chat.ts                 # Chat API functions
│   │   ├── auth.ts                 # Auth API functions
│   │   ├── documents.ts            # Documents API functions
│   │   ├── email.ts                # Email API functions (if available)
│   │   ├── calendar.ts             # Calendar API functions (if available)
│   │   └── sse.ts                  # SSE stream handler
│   ├── hooks/
│   │   ├── useChat.ts              # Chat state management hook
│   │   ├── useSSE.ts               # SSE streaming hook
│   │   ├── useAuth.ts              # Authentication hook
│   │   ├── useVoice.ts             # Voice input/output hook
│   │   ├── useLocalStorage.ts     # LocalStorage hook
│   │   ├── useDocuments.ts         # Documents management hook
│   │   ├── useEmail.ts             # Email integration hook
│   │   ├── useCalendar.ts          # Calendar integration hook
│   │   ├── useMemory.ts            # Memory/facts hook
│   │   ├── useCommandPalette.ts    # Command palette hook
│   │   ├── useKeyboardShortcuts.ts # Keyboard shortcuts hook
│   │   └── useNotifications.ts     # Notifications hook
│   ├── utils/
│   │   ├── formatDate.ts           # Date formatting utilities
│   │   ├── markdown.ts             # Markdown processing
│   │   └── constants.ts            # App constants
│   └── context/
│       ├── ChatContext.tsx          # Chat state context
│       ├── AuthContext.tsx          # Auth state context
│       ├── SettingsContext.tsx     # Settings context
│       ├── DocumentsContext.tsx     # Documents state context
│       ├── MemoryContext.tsx        # Memory/facts context
│       └── NotificationContext.tsx  # Notifications context
├── styles/
│   ├── globals.css                  # Global styles + Tailwind + DM Sans import
│   └── animations.css               # Custom animations (fadeIn, typing, etc.)
├── public/
│   ├── icons/
│   │   ├── icon-192x192.png
│   │   ├── icon-512x512.png
│   │   └── apple-touch-icon.png
│   ├── manifest.json                # PWA manifest
│   └── sw.js                         # Service worker (or use next-pwa)
├── types/
│   ├── api.ts                       # API response types
│   ├── chat.ts                      # Chat-related types
│   ├── user.ts                      # User types
│   ├── documents.ts                 # Document types
│   ├── email.ts                     # Email types
│   ├── calendar.ts                  # Calendar types
│   └── memory.ts                    # Memory/facts types
├── .env.local.example                # Environment variables example
├── next.config.js                    # Next.js configuration
├── tailwind.config.js                # Tailwind configuration
├── tsconfig.json                     # TypeScript configuration
├── package.json                      # Dependencies
└── README.md                         # Setup instructions
```

### Naming Conventions
**CRITICAL**: Use meaningful, descriptive names. Avoid generic names like:
- ❌ `container`, `wrapper`, `group`, `div`, `section`
- ❌ `Component1`, `Component2`, `Item`, `Box`
- ✅ `ChatMessage`, `SidebarNavigation`, `ModelSelector`, `SettingsPanel`

**File Naming**:
- Components: PascalCase (e.g., `ChatMessage.tsx`)
- Utilities: camelCase (e.g., `formatDate.ts`)
- Hooks: camelCase with `use` prefix (e.g., `useChat.ts`)
- Types: camelCase (e.g., `api.ts`)

**Function Naming**:
- React components: PascalCase
- Functions: camelCase with descriptive verbs (e.g., `handleSendMessage`, `fetchChatHistory`)
- Constants: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)

### Code Quality Standards
- **TypeScript**: Strict mode enabled, no `any` types
- **ESLint**: Next.js recommended rules
- **Prettier**: Consistent code formatting
- **Comments**: JSDoc comments for complex functions
- **Error Handling**: Try-catch blocks, error boundaries
- **Loading States**: Skeleton loaders, loading spinners
- **Error States**: User-friendly error messages
- **Accessibility**: ARIA labels, keyboard navigation, focus management

## Functional Requirements

### Chat Functionality
1. **Send Message**
   - Validate input (non-empty, max length)
   - Show loading state
   - Stream response via SSE
   - Update UI in real-time
   - Handle errors gracefully
   - Save to local state and sync with backend

2. **Chat History**
   - Load history on session start
   - Display in sidebar
   - Click to switch conversations
   - Auto-save current conversation
   - Persist in localStorage as backup

3. **New Chat**
   - Clear current messages
   - Generate new session ID
   - Reset input
   - Update history list

4. **Streaming Response**
   - Parse SSE events correctly
   - Display chunks as they arrive
   - Show tool execution indicators
   - Handle stream errors
   - Mark stream completion

### Authentication
1. **Login Flow**
   - Email/password form
   - OAuth buttons (Google, Microsoft) - if backend supports
   - Store JWT token
   - Redirect to chat on success
   - Show error messages

2. **Signup Flow**
   - Registration form with validation
   - Password strength indicator
   - Terms acceptance
   - Auto-login after signup

3. **Auth State**
   - Check token on app load
   - Auto-logout on token expiry
   - Protected routes
   - Show user info in sidebar

### Voice Features
1. **Voice Input**
   - Click microphone to start
   - Visual recording indicator
   - Stop recording on click again
   - Send audio to transcription API
   - Insert transcribed text into input

2. **Voice Output** (Optional)
   - Toggle in settings
   - Play audio response
   - Show audio controls

### Settings Management
1. **Context/System Prompt**
   - Save to localStorage
   - Send with each chat request (if backend supports)
   - Clear/reset option
   - Character count
   - Preset templates

2. **Model Selection**
   - Store in localStorage
   - Send with chat request (if backend supports)
   - Show current selection
   - Model status indicator

3. **Preferences**
   - Persist all settings
   - Apply immediately
   - Reset to defaults option
   - Export/import settings

### Documents Management
1. **Upload Documents**
   - Drag & drop interface
   - File picker
   - Upload progress tracking
   - File validation (PDF, DOCX)
   - Multiple file upload

2. **Document List**
   - View all uploaded documents
   - Document metadata (name, size, date)
   - Processing status
   - Delete documents
   - Re-index documents

3. **Document Integration**
   - Show document count in sidebar
   - Quick access to documents
   - Document status indicators

### Email Integration (Microsoft 365)
1. **Email Quick View**
   - Recent emails list
   - Unread count badge
   - Email preview
   - Quick actions (read, compose)

2. **Email Actions**
   - "Read my emails" command
   - "Compose email" command
   - Email search

3. **Connection Status**
   - M365 connection indicator
   - Last sync time
   - Reconnect option

### Calendar Integration (Microsoft 365)
1. **Calendar Quick View**
   - Upcoming events
   - Today's events
   - Event details

2. **Calendar Actions**
   - "View calendar" command
   - "Schedule meeting" command
   - Create event from chat

### Memory/Facts Management
1. **View Facts**
   - List all stored facts
   - Search facts
   - Fact categories (if supported)

2. **Manage Facts**
   - Add new fact
   - Edit existing fact
   - Delete fact
   - Export/import facts

3. **Fact Integration**
   - Show facts count in sidebar
   - Quick access to facts manager
   - Facts used in conversation indicator

## Performance Requirements
- **Initial Load**: < 2 seconds
- **Time to Interactive**: < 3 seconds
- **Lighthouse Score**: > 90 for all categories
- **Code Splitting**: Route-based and component-based
- **Image Optimization**: Next.js Image component
- **Bundle Size**: Minimize dependencies
- **Caching**: Aggressive caching for static assets

## Browser Support
- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Additional Features to Include

### Command Palette (Cmd/Ctrl + K)
- **Search & Navigation**:
  - Search conversations
  - Quick actions
  - Navigate to settings
  - Open documents manager
- **Commands**:
  - `/new` - New chat
  - `/settings` - Open settings
  - `/docs` - Documents manager
  - `/memory` - Memory/facts manager
  - `/email` - Email quick view
  - `/calendar` - Calendar view
  - `/export` - Export conversation
- **Fuzzy Search**: Intelligent matching
- **Keyboard Navigation**: Arrow keys to navigate, Enter to select

### Documents Manager Panel
- **Upload Section**:
  - Drag & drop area
  - File picker button
  - Supported formats: PDF, DOCX
  - Upload progress for each file
- **Documents List**:
  - Document name, size, upload date
  - Processing status (Processing/Ready/Error)
  - Delete button
  - Re-index button
  - Preview button (if supported)
- **Statistics**:
  - Total documents
  - Total size
  - Index status

### Email Integration Panel
- **Quick View** (Slide-in panel):
  - Recent emails list (from M365)
  - Unread count badge
  - Email preview (subject, sender, snippet)
  - Mark as read button
  - Compose email button (opens in chat with pre-filled prompt)
- **Email Actions**:
  - "Read my emails" - Quick command
  - "Compose email to..." - Quick compose
  - Email search

### Calendar Integration Panel
- **Quick View** (Slide-in panel):
  - Upcoming events (next 7 days)
  - Today's events highlighted
  - Event details (title, time, location, attendees)
  - Create event button (opens in chat)
- **Calendar Actions**:
  - "What's on my calendar?" - Quick query
  - "Schedule meeting..." - Quick schedule
  - Month/week view toggle

### Memory/Facts Manager Panel
- **Facts List**:
  - Key-value pairs display
  - Search/filter facts
  - Group by category (if supported)
- **Actions**:
  - Add new fact
  - Edit existing fact
  - Delete fact
  - Export all facts
  - Import facts
- **Statistics**:
  - Total facts count
  - Recently added facts

### Conversation Features
- **Message Actions**:
  - Copy message
  - Copy entire conversation
  - Regenerate response
  - Edit & resend user message
  - Delete message (with confirmation)
  - Pin important messages
- **Conversation Actions**:
  - Export conversation (JSON, PDF, Markdown)
  - Share conversation (generate shareable link)
  - Duplicate conversation
  - Archive conversation
  - Search within conversation (`Cmd/Ctrl + F`)
- **Message Feedback**:
  - Thumbs up/down buttons
  - Feedback submission (optional text)
  - Store feedback for improvement

### Notification Center
- **Notifications**:
  - New email alerts
  - Calendar event reminders
  - Document processing complete
  - System notifications
- **Notification Panel**:
  - Slide-in from top or side
  - Unread count badge
  - Mark all as read
  - Notification history
  - Settings link

### Usage Statistics Dashboard
- **Metrics Display** (in Settings or separate panel):
  - Total messages sent
  - Total conversations
  - Documents uploaded
  - Facts stored
  - API calls made
  - Usage over time (charts)
  - Most used features

### Error Handling
- Network error messages with retry button
- API error handling with user-friendly messages
- Offline detection with offline indicator
- Retry mechanisms with exponential backoff
- Error boundaries with fallback UI
- Connection status indicator (top bar)
- Error logging for debugging

### Loading States
- Skeleton loaders for initial load
- Spinner for actions
- Progress indicators for long operations
- Upload progress bars
- Document processing indicators
- Smooth loading transitions

### Animations
- Smooth page transitions
- Message appearance animations (fade in, slide up)
- Button hover effects with scale
- Sidebar slide animations
- Typing indicator animation
- Tool execution pulse animation
- Success/error toast notifications
- Loading shimmer effects

### Accessibility
- Keyboard navigation (full support)
- Screen reader support (ARIA labels)
- Focus management (visible focus indicators)
- ARIA labels on all interactive elements
- Color contrast compliance (WCAG AA minimum)
- Skip to content link
- Reduced motion support (respect prefers-reduced-motion)
- High contrast mode support

## Deliverables
The generated code must be:
1. **Complete**: All files necessary to run the application
2. **Functional**: Works out of the box with minimal setup
3. **Clean**: No unnecessary files, comments, or code
4. **Professional**: Production-ready code quality
5. **Documented**: README with setup instructions
6. **Configurable**: Environment variables for API URL
7. **Tested**: Basic functionality verified (manual testing notes)

## Setup Instructions to Include
The generated project should include a README.md with:
- Installation steps (`npm install` or `yarn install`)
- Environment variable setup
- Development server start command
- Build command
- Production deployment notes
- API integration notes

## Feature Summary

### Core Features
✅ Full-screen ChatGPT-like interface
✅ Responsive design (mobile, tablet, desktop)
✅ Left sidebar with chat history
✅ New chat functionality
✅ Settings panel
✅ Model selector dropdown
✅ Voice input/output
✅ Document upload and management
✅ Markdown rendering with syntax highlighting
✅ Real-time streaming responses (SSE)
✅ Tool execution indicators

### Advanced Features
✅ **Command Palette** (Cmd/Ctrl + K) - Quick actions and search
✅ **Documents Manager** - Upload, view, delete documents
✅ **Email Integration** - Quick email access (M365)
✅ **Calendar Integration** - View and manage events (M365)
✅ **Memory/Facts Manager** - Store and manage personal facts
✅ **Conversation Management** - Export, share, search, pin conversations
✅ **Message Actions** - Copy, regenerate, edit, feedback
✅ **Notification Center** - System and integration notifications
✅ **Usage Statistics** - Track usage and metrics
✅ **Keyboard Shortcuts** - Comprehensive shortcut support
✅ **Quick Actions Panel** - One-click common tasks
✅ **Search Functionality** - Search conversations and facts
✅ **Export Options** - Export conversations, facts, settings
✅ **Rich Content Support** - Tables, lists, links, email/calendar previews

### Integration Features
✅ Microsoft 365 connection status
✅ Email quick view with unread count
✅ Calendar quick view with upcoming events
✅ Document processing status
✅ API health monitoring
✅ Connection status indicators

### UX Enhancements
✅ Glass morphism design throughout
✅ Smooth animations and transitions
✅ Loading states and skeleton loaders
✅ Error handling with retry mechanisms
✅ Offline detection and support
✅ Accessibility (WCAG AA compliant)
✅ PWA support with offline capabilities
✅ Toast notifications
✅ Tooltips and help text
✅ Welcome screen with example prompts

## Design Quality Checklist
- ✅ **Rounded Corners**: Every element must have appropriate border-radius (12px, 18px, 20px, 25px)
- ✅ **Clear Visibility**: High contrast text, readable fonts, proper spacing
- ✅ **Chat Bubbles**: 
  - User: Purple gradient (#667eea to #764ba2), white text, 18px radius with 4px tail
  - AI: White background, dark text (#333), 18px radius with 4px tail
- ✅ **Typography**: DM Sans font family throughout, proper weights (400, 500, 600, 700)
- ✅ **Spacing**: Generous padding (12-20px), clear gaps between elements
- ✅ **Shadows**: Subtle elevation with proper shadow levels
- ✅ **Transitions**: Smooth 200-300ms transitions on all interactive elements
- ✅ **Focus States**: Visible focus indicators on all interactive elements
- ✅ **Color Consistency**: Purple gradient theme (#667eea to #764ba2) used consistently
- ✅ **Liquid Glass Morphism**: Advanced glass effects with blur, transparency, inner glow, and liquid gradients
- ✅ **Depth & Layering**: Multiple layers with proper shadows and elevation
- ✅ **Modern AI Patterns**: Inspired by OKAI, Omni Agent, and liquid glass designs
- ✅ **Smooth Animations**: Flowing, liquid-like transitions where appropriate

## Design Inspiration Implementation

### Liquid Glass Effects (From Dribbble Inspiration)
- **Advanced Blur**: Use `backdrop-blur-2xl` (40px) for maximum glass effect
- **Layered Transparency**: Multiple layers with varying opacity (0.05, 0.08, 0.1, 0.15)
- **Inner Glow**: `inset 0 1px 0 rgba(255, 255, 255, 0.1)` for depth
- **Gradient Overlays**: Subtle gradients from top-left to bottom-right
- **Reflection Highlights**: Subtle white highlights on top edges
- **Colored Shadows**: Purple-tinted shadows for cohesion

### Modern AI Chatbot Patterns (From OKAI & Omni Agent)
- **Conversation Flow**: Smooth message appearance with staggered animations
- **Tool Indicators**: Prominent, color-coded tool execution badges
- **Status Indicators**: Clear visual feedback for all states
- **Dashboard Elements**: Information cards with glass morphism
- **Quick Actions**: Prominent, accessible action buttons
- **Context Awareness**: Visual indicators for context and memory usage

### Premium Polish
- **Micro-interactions**: Subtle hover effects, click feedback, loading states
- **Smooth Scrolling**: Custom scrollbars with glass styling
- **Loading States**: Elegant skeleton loaders and spinners
- **Error States**: Beautiful error messages with clear actions
- **Empty States**: Engaging empty states with helpful guidance

## Final Notes
- The UI should feel **premium, modern, and AI-powered** like OKAI and Omni Agent
- **Match the current frontend design**: Rounded corners everywhere, clear visibility, beautiful chat bubbles
- **DM Sans font** must be used throughout for consistency
- Purple gradient theme (#667eea to #764ba2) should be consistent throughout
- **Liquid glass morphism** should enhance, not distract - use advanced blur and transparency
- All interactions should be **smooth and responsive** with flowing animations
- Chat bubbles must have the characteristic rounded corners with one smaller corner (4px) for tail effect
- Text must be highly readable with excellent contrast
- **Depth & Layering**: Use multiple layers, shadows, and elevation for 3D effect
- The code should be maintainable and scalable
- Follow React and Next.js best practices
- Use TypeScript strictly (no `any` types)
- Implement proper error boundaries
- Add loading and error states everywhere
- Make it feel like a **professional AI assistant interface** (inspired by modern platforms)
- All features should be intuitive and discoverable
- Performance should be optimized (lazy loading, code splitting)
- All user data should be handled securely
- Provide clear feedback for all user actions
- **Visual Polish**: Every element should look polished with proper spacing, shadows, rounded corners, and liquid glass effects
- **Reference the design inspirations** throughout development for consistency

---

**Generate a complete, production-ready Next.js application that I can download and use immediately. All code should be clean, well-structured, and follow the specifications above exactly. Include all the features listed in this prompt.**

