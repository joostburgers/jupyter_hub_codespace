# Flythrough Instructions — Project 5: Mapping Emotions

> **Collaborative note:** Chapters in `flythrough_config.js` are pre-labeled with which team member should edit them (e.g., `// ===== MEMBER 2 EDITS THIS CHAPTER =====`). Only edit the chapters assigned to you. See [COLLABORATION_GUIDE.md](COLLABORATION_GUIDE.md) for full workflow guidance.

## Overview
This version uses **OpenStreetMap** and **Leaflet** instead of Mapbox, so you don't need any API tokens or accounts. Everything is completely free!

## Quick Start

### Files You Need:
1. `flythrough_config.js` - Your story configuration 
2. `flythrough_template.html` - The interactive map template
3. Your processed sentiment data (from CSV)
4. Images for your story (in `./images/` folder)

### Immediate Setup:
1. **Open** `flythrough_template.html` in any web browser
2. **It works instantly** - no API keys needed!
3. **Customize** the `flythrough_config.js` file with your data

## Understanding the Structure

The flythrough is built around **chapters** - each chapter represents one view/stop in your story. There are two types of chapters:

### Overview Chapters (Camera Only)
These show a view without placing a marker on the map. Use for introductions, transitions, and conclusions.

```javascript
{
    id: 'intro',
    title: 'Campus Sentiment Overview',
    description: 'Exploring student feelings about campus locations...',
    image: './images/quad.jpg',
    duration: 3000,
    
    camera: {                    // Where the map flies to
        latitude: 38.4365,
        longitude: -78.8705,
        zoom: 14                 // Lower = zoomed out, higher = zoomed in
    },
    
    showData: 'all_locations'    // Show all location markers
}
```

### Location Chapters (Camera + Data)
These fly to a specific location AND display its data marker.

```javascript
{
    id: 'dhall',
    title: 'D-Hall: The Social Hub',
    description: 'Students have mixed feelings about D-Hall...',
    image: './images/dhall.jpg',
    duration: 2000,
    
    camera: {                    // Where the map flies to
        latitude: 38.4335,
        longitude: -78.8715,
        zoom: 17
    },
    
    location: {                  // Data point to display (from CSV)
        name: 'D-Hall',
        latitude: 38.4335,       // Must match camera coordinates
        longitude: -78.8715,
        postCount: 156,          // From your CSV
        robertaScore: -0.12,     // From your CSV
        isJMU: true              // true = JMU, false = UNC (or other school)
    },
    
    showData: 'individual'       // Highlight only this location
}
```

## Customizing Your Flythrough

### 1. Change Map Style
In `flythrough_config.js`, uncomment your preferred map style:

```javascript
// Positron Light (default - clean minimal style)
tileLayer: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',

// Dark Positron (dark theme)
// tileLayer: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',

// Standard OpenStreetMap (classic map style)
// tileLayer: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

// Terrain (topographic map)
// tileLayer: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
```

### 2. Choose Color Scale
Pick how sentiment is colored on the map:

```javascript
colorScale: 'RdYlGn',  // Red (negative) → Yellow → Green (positive)
// OR
colorScale: 'Portland',  // Blue (negative) → White → Red (positive)
```

### 3. Fill In Your Chapters

The template includes 10 pre-structured chapters. Each chapter comment shows assignments for both team sizes — read the column that matches yours:

| Chapter | Content | 4-Member Team | 5-Member Team |
|---------|---------|---------------|---------------|
| 1. Intro | Wide view of both campuses | Member 1 | Member 1 |
| 2. JMU Campus | Overview of JMU locations | Member 2 | Member 2 |
| 3. JMU Location 1 | Individual JMU location | Member 2 | Member 2 |
| 4. JMU Location 2 | Individual JMU location | Member 2 | Member 3 |
| 5. JMU Location 3 | Individual JMU location | Member 3 | Member 3 |
| 6. Other School Campus | Overview of other school | Member 3 | Member 4 |
| 7. Other School Location 1 | Individual location | Member 4 | Member 4 |
| 8. Other School Location 2 | Individual location | Member 4 | Member 5 |
| 9. Other School Location 3 | Individual location | Member 4 | Member 5 |
| 10. Conclusion | Wide wrap-up view | Member 1 | Member 1 |

**For each location chapter:**
1. Copy latitude/longitude from your CSV
2. Use the same coordinates for both `camera` and `location`
3. Look at your whitepaper map/visualizations to find `postCount` and `robertaScore` for each location
4. Replace placeholder titles and descriptions
5. Add appropriate images to `./images/` folder

### 4. Understanding showData Options

- `'all_locations'` - Shows all markers from all chapters
- `'jmu_locations'` - Shows only markers where `isJMU: true`
- `'non_jmu_locations'` - Shows only markers where `isJMU: false`
- `'individual'` - Highlights only the current chapter's location marker

### 5. HTML Support in Text

Both `title` and `description` support HTML formatting:

```javascript
title: 'D-Hall: The <em>Social</em> Hub',
description: 'Students report <strong>mixed emotions</strong>.<br><br>Positive: social connections<br>Negative: food quality'
```

## Adding Images

1. **Add your photos** to the `./images/` folder (JPG, PNG, GIF supported)
2. **Reference them** in your config:

```javascript
{
    id: 'chapter-1',
    title: 'Your Location',
    image: './images/your-photo.jpg',  // Relative path
    description: '...',
    camera: { /* ... */ }
}
```

## Testing Your Flythrough

### Local Testing:
1. **Open** `flythrough_template.html` in your web browser
2. **Scroll down** to navigate through your story
3. **Check the browser console** (F12) for any errors

### Common Issues:

**Map doesn't load:**
- Check browser console for errors
- Ensure internet connection (map tiles load from web)

**Markers don't appear:**
- Verify you have `location` objects in chapters where you want markers
- Check that coordinates are correct numbers (not strings)
- Ensure `postCount` is not null for data chapters
- Look for JavaScript syntax errors in console

**Camera doesn't fly:**
- Ensure each chapter has a `camera` object
- Check `duration` values are numbers in milliseconds
- Verify coordinates are valid numbers

**Images don't show:**
- Check file paths are correct (`./images/filename.jpg`)
- Ensure images exist in the `images` folder
- Verify file extensions match exactly

## Deployment Options

### GitHub Pages (Recommended):
1. Create a GitHub repository
2. Upload all your files
3. Go to Settings → Pages
4. Select "Deploy from a branch" → main
5. Your flythrough will be live at `username.github.io/repository-name`

### Alternative Free Hosting:
- **Netlify:** Drag and drop your folder
- **Vercel:** Connect your GitHub repo

## Quick Reference

### Zoom Levels:
- `6-8`: Regional view (multiple cities)
- `12-14`: City/campus overview
- `16-18`: Individual building close-up

### Duration (milliseconds):
- `2000`: Fast transition (2 seconds)
- `2500`: Medium transition
- `3000`: Slow transition (3 seconds)

### Data Collection:
All location data automatically collected from chapters with `location` objects. No need to duplicate data!

### isJMU Property:
- `true`: Location belongs to JMU (or your primary school)
- `false`: Location belongs to comparison school (UNC, etc.)

## Support Resources

- **Leaflet Documentation:** [leafletjs.com](https://leafletjs.com)
- **OpenStreetMap:** [openstreetmap.org](https://openstreetmap.org)
- **Free Map Styles:** [leaflet-extras.github.io/leaflet-providers/](https://leaflet-extras.github.io/leaflet-providers/)

---

**🎉 You're all set!** Your flythrough will automatically display all location markers and fly between chapters as users scroll.