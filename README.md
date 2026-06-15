# Garden Stress Monitor AR

Real-time plant stress detection visualization in AR using point cloud data from your garden.

**Coordinates:** 40.33105186237493°N, 44.59644202143014°E (Bulgaria)

## Features

- **10,000 point cloud** representing garden sensor data
- **131 stressed plants** detected and highlighted in red
- **Real-time AR visualization** on iOS Safari and Android
- **Point cloud rendering** with health-based color coding:
  - 🟢 Green points = Healthy plants (NDRE: 0.4-0.6)
  - 🔴 Red points = Stressed plants (NDRE: 0.1-0.25)

## Files

- `garden.html` - Main AR interface
- `pointcloud.glb` - 3D point cloud model (10,000 points)
- `pipeline.py` - Python script to generate mock data
- `pointcloud.py` - Point cloud generation script

## Quick Start (Local)

### Option 1: Local Network (WiFi)

1. **Start HTTP server** (keep running):
   ```powershell
   cd C:\Users\mshet.000\Desktop\AR
   python -m http.server 8080
   ```

2. **On your iPhone**, open Safari and go to:
   ```
   http://192.168.1.60:8080/garden.html
   ```

3. Tap **"Launch AR Camera"** to visualize the point cloud in 3D space

### Option 2: Public Internet (Mobile Data)

Deploy to **GitHub Pages** (free, instant):

#### Step 1: Create GitHub Repository
```bash
# If you haven't authenticated with GitHub yet
gh auth login

# Create a new public repository
gh repo create garden-stress-ar --public --source=. --remote=origin --push
```

#### Step 2: Enable GitHub Pages
Go to your GitHub repository → Settings → Pages → Source: **main branch** → Save

Your site will be live at: `https://[your-github-username].github.io/garden-stress-ar/garden.html`

---

## Alternative: Deploy to Netlify (Even Easier)

1. **Drag and drop to Netlify:**
   - Go to https://app.netlify.com/drop
   - Drag the entire `AR` folder
   - Get instant HTTPS URL

2. **Or use Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   netlify deploy --dir=. --public
   ```

---

## Alternative: Deploy to Vercel

```bash
npm install -g vercel
vercel --prod
```

Instant global CDN, HTTPS included.

---

## iOS Safari AR Requirements

- iOS 12+ (iPhone/iPad)
- Safari browser
- **HTTPS URL required** (not HTTP)
- AR Quick Look support enabled

## Android Requirements

- Android 7.0+
- Google Chrome or equivalent
- ARCore support

## Technical Details

### Point Cloud Format

- **Total points:** 10,000
- **Dimensions:** 10m × 10m × 3m (garden width × length × canopy height)
- **Stress zone:** Center at [5.0, 5.0, 0.5]m with 1.0m radius
- **Format:** GLB (GL Transmission Format)

### Visualization

Each point is rendered as a small sphere:
- **Green spheres** = NDRE > 0.35 (healthy)
- **Red spheres** = NDRE < 0.25 (stressed)

### Model Viewer

Uses Google's `<model-viewer>` library for cross-platform AR support:
- iOS: AR Quick Look
- Android: Scene Viewer / ARCore
- Desktop: WebGL preview

---

## Development

### Regenerate Point Cloud

```bash
python pointcloud.py
```

Updates `pointcloud.glb` with new random point data.

### Regenerate Stress Hotspot

Edit `pointcloud.py` and modify:
```python
stress_center = np.array([5.0, 5.0, 0.5])  # Center coordinates
stress_radius = 1.0  # Detection radius in meters
```

Then run: `python pointcloud.py`

---

## Troubleshooting

### "Server can't be found"
- Verify iPhone is on same WiFi as PC
- Check PC IP: `ipconfig | findstr IPv4`
- Ensure HTTP server is running: `netstat -ano | findstr 8080`

### "White points instead of colored"
- Refresh the page (pull down on Safari)
- Clear Safari cache: Settings → Safari → Clear History
- Regenerate model: `python pointcloud.py`

### AR doesn't activate
- Use HTTPS URL (local IP won't support AR)
- Deploy to GitHub Pages / Netlify / Vercel
- Ensure you're on iOS 12+ or Android 7.0+

---

## Next Steps

1. **Deploy to public internet** (GitHub Pages / Netlify)
2. **Test in your garden** with real GPS coordinates
3. **Integrate real sensor data** from IoT devices
4. **Add time-series visualization** for stress trends

---

Made with AR.js and model-viewer 🌱
