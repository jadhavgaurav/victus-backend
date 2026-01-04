# Mobile & Cross-Platform Support - VICTUS

## ✅ Cross-Platform System Tools

VICTUS now supports **Windows, macOS, and Linux** for all system operations!

### Supported Platforms

#### ✅ Windows
- All original features work
- Registry-based app detection
- Microsoft Store apps
- Full system control

#### ✅ macOS
- Native app launching via `open` command
- Spotlight search for apps
- macOS-specific apps (Safari, Finder, Xcode, etc.)
- Screenshot via `screencapture`
- Window detection via AppleScript

#### ✅ Linux
- Desktop file launching
- PATH-based app detection
- XDG standard folders
- Multiple screenshot tools (gnome-screenshot, scrot, maim)
- Window detection via xdotool/wmctrl

### System Tools Available

| Tool | Windows | macOS | Linux | Mobile |
|------|---------|-------|-------|--------|
| `list_files` | ✅ | ✅ | ✅ | ✅ (via PWA) |
| `open_app` | ✅ | ✅ | ✅ | ⚠️ Limited |
| `get_clipboard_content` | ✅ | ✅ | ✅ | ✅ (via Clipboard API) |
| `take_screenshot` | ✅ | ✅ | ✅ | ✅ (via MediaDevices API) |
| `type_text` | ✅ | ✅ | ✅ | ❌ (Security) |
| `get_active_window_title` | ✅ | ✅ | ✅ | ❌ (Not applicable) |
| `get_system_info` | ✅ | ✅ | ✅ | ✅ |

## 📱 Mobile Support (PWA)

### ✅ What Works on Mobile

1. **PWA Installation**
   - Install as app on iOS and Android
   - Works offline (cached pages)
   - App-like experience

2. **File Operations**
   - List files (via file picker)
   - Upload documents
   - View file contents

3. **Clipboard**
   - Read clipboard (with permission)
   - Copy to clipboard

4. **Screenshots**
   - Take screenshots (with permission)
   - Save to device

5. **Voice Interface**
   - Speech-to-text (browser API)
   - Text-to-speech (browser API)

6. **All Web Features**
   - Chat interface
   - Email management
   - Calendar operations
   - Document querying
   - Memory/facts

### ⚠️ Mobile Limitations

**Cannot Do (Security Restrictions):**
- ❌ Direct app launching (browser security)
- ❌ System-level automation (type_text)
- ❌ Window management (not applicable)
- ❌ File system access (limited to user-selected files)

**Workarounds:**
- Use deep links for common apps (e.g., `tel:`, `mailto:`, `sms:`)
- Use Web Share API for sharing content
- Use File System Access API (limited browser support)

## 🔧 Mobile-Specific Features

### Deep Links (Mobile)

The PWA can use deep links to open apps:

```javascript
// Phone call
window.location.href = 'tel:+1234567890';

// Email
window.location.href = 'mailto:user@example.com';

// SMS
window.location.href = 'sms:+1234567890';

// Maps
window.location.href = 'https://maps.google.com/?q=location';

// Calendar (iOS)
window.location.href = 'calshow://';

// Settings (iOS)
window.location.href = 'app-settings://';
```

### Web APIs for Mobile

1. **Clipboard API**
   ```javascript
   navigator.clipboard.readText()
   navigator.clipboard.writeText()
   ```

2. **MediaDevices API**
   ```javascript
   navigator.mediaDevices.getDisplayMedia() // Screen capture
   ```

3. **File System Access API**
   ```javascript
   window.showOpenFilePicker()
   window.showSaveFilePicker()
   ```

4. **Web Share API**
   ```javascript
   navigator.share({ title, text, url })
   ```

## 🚀 Mobile App Development (Future)

### Native Apps

For full system control, native apps would be needed:

#### Android
- **Language**: Kotlin/Java
- **Framework**: Android SDK
- **Features**: Full system access, background services
- **Distribution**: Google Play Store

#### iOS
- **Language**: Swift
- **Framework**: iOS SDK
- **Features**: Limited system access (iOS restrictions)
- **Distribution**: App Store

### Hybrid Approach

**React Native / Flutter:**
- Cross-platform mobile apps
- Can access native APIs
- Share codebase with web
- Full system control possible

## 📋 Platform-Specific App Aliases

### macOS Apps
- Safari, Finder, Terminal
- Xcode, Pages, Numbers, Keynote
- Music, Photos, Messages
- Calculator, TextEdit

### Linux Apps
- gnome-terminal, nautilus
- gedit, vim, nano
- firefox, chrome
- rhythmbox, shotwell

### Windows Apps
- All original Windows apps
- Microsoft Store apps
- Traditional .exe applications

## 🔐 Security Considerations

### Desktop (Full Access)
- ✅ System-level operations allowed
- ✅ App launching
- ✅ File system access
- ✅ Automation

### Mobile (Limited Access)
- ⚠️ Browser security restrictions
- ⚠️ User permission required
- ⚠️ Limited file system access
- ⚠️ No direct app control

## 📝 Implementation Notes

### Detecting Platform

```python
import platform

IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"
```

### Mobile Detection (Frontend)

```javascript
const isMobile = /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
const isAndroid = /Android/.test(navigator.userAgent);
```

## ✅ Summary

**Desktop (Windows/macOS/Linux):**
- ✅ Full system control
- ✅ All tools available
- ✅ App launching
- ✅ Automation

**Mobile (PWA):**
- ✅ Core features work
- ✅ File operations (limited)
- ✅ Clipboard access
- ✅ Screenshots
- ⚠️ No direct app control
- ⚠️ Limited automation

**Future Native Apps:**
- Full system control on mobile
- Background services
- Native integrations
- App store distribution

---

**All Windows tasks can now be performed on macOS!** 🎉

