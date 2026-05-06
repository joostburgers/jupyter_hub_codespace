// OpenStreetMap-based Flythrough Configuration
// No API tokens required - uses free OpenStreetMap tiles via Leaflet

var config = {
    // =============================================================================
    // MAP STYLE SETTINGS
    // To change style: comment out current tileLayer and uncomment your choice
    // =============================================================================
    
    // Positron Light (clean minimal style, perfect for data visualization)
    tileLayer: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    
    // Dark Positron (dark theme)
    // tileLayer: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    
    // Standard OpenStreetMap (classic map style)
    // tileLayer: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    
    // Terrain (topographic map)
    // tileLayer: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    
    // =============================================================================
    // COLOR SCALE SETTINGS (Choose one - Plotly inspired)
    // =============================================================================
    
    colorScale: 'RdYlGn',  // Options: 'RdYlGn' (Red-Yellow-Green) or 'Portland' (Blue-White-Red)
    
    // =============================================================================
    // STORY CHAPTERS
    // Students: Fill in with your data
    // - Coordinates: Get from your CSV file (latitude, longitude columns)
    // - Post counts & sentiment scores: Look up in your whitepaper visualizations
    // =============================================================================
    
    chapters: [
        {
            // ===== ALL TEAM SIZES: Member 1 =====
            // CHAPTER 1: Overview of both locations
            id: 'intro',
            title: 'Reddit Sentiment Analysis: Two College Towns',
            description: 'Exploring how students discuss their campuses on Reddit - comparing JMU in Harrisonburg, VA and UNC in Chapel Hill, NC.',
            image: './images/quad.jpg',
            duration: 3000,
            
            // Camera position (where to fly)
            camera: {
                latitude: 37.2,             // Midpoint between JMU and UNC
                longitude: -78.0,
                zoom: 8                     // Wide view showing both locations
            },
            
            showData: 'all_locations'       // Show all locations from both schools
        },
        
        {
            // ===== 4-MEMBER TEAM: Member 2 | 5-MEMBER TEAM: Member 2 =====
            // CHAPTER 2: JMU Campus Overview
            id: 'jmu-campus',
            title: 'JMU Campus Overview',
            description: 'James Madison University in Harrisonburg, Virginia. Three key locations emerge from student discussions.',
            image: './images/d_hall.jpg',
            duration: 2500,
            
            // Camera position
            camera: {
                latitude: 38.4365,
                longitude: -78.8705,
                zoom: 14
            },
            
            showData: 'jmu_locations'       // Show only JMU locations
        },
        
        {
            // ===== 4-MEMBER TEAM: Member 2 | 5-MEMBER TEAM: Member 2 =====
            // CHAPTER 3: JMU Location 1
            id: 'jmu-location-1',
            title: 'JMU Location 1: [Name Here]',
            description: 'Add your description here. Include sentiment analysis findings, post count, and key themes.',
            image: './images/quad.jpg',
            duration: 2000,
            
            // Camera position
            camera: {
                latitude: 38.4347,           // Replace with coordinates from CSV
                longitude: -78.8690,
                zoom: 17
            },
            
            // Location data (creates the marker on map)
            location: {
                name: 'JMU Location 1',      // Replace with location name from CSV
                latitude: 38.4347,           // Must match camera coordinates
                longitude: -78.8690,
                postCount: 50,               // Look up in your whitepaper visualizations
                robertaScore: 0.25,          // Look up in your whitepaper visualizations
                isJMU: true
            },
            
            showData: 'individual'           // Highlight only this location
        },
        
        {
            // ===== 4-MEMBER TEAM: Member 2 | 5-MEMBER TEAM: Member 3 =====
            // CHAPTER 4: JMU Location 2
            id: 'jmu-location-2',
            title: 'JMU Location 2: [Name Here]',
            description: 'Add your description here.',
            image: './images/arboretum.jpg',
            duration: 2000,
            
            camera: {
                latitude: 38.4335,
                longitude: -78.8715,
                zoom: 17
            },
            
            location: {
                name: 'JMU Location 2',
                latitude: 38.4335,
                longitude: -78.8715,
                postCount: 75,
                robertaScore: -0.15,
                isJMU: true
            },
            
            showData: 'individual'
        },
        
        {
            // ===== 4-MEMBER TEAM: Member 3 | 5-MEMBER TEAM: Member 3 =====
            // CHAPTER 5: JMU Location 3
            id: 'jmu-location-3',
            title: 'JMU Location 3: [Name Here]',
            description: 'Add your description here.',
            image: './images/art_gallery.jpg',
            duration: 2000,
            
            camera: {
                latitude: 38.4390,
                longitude: -78.8620,
                zoom: 17
            },
            
            location: {
                name: 'JMU Location 3',
                latitude: 38.4390,
                longitude: -78.8620,
                postCount: 100,
                robertaScore: 0.55,
                isJMU: true
            },
            
            showData: 'individual'
        },
        
        {
            // ===== 4-MEMBER TEAM: Member 3 | 5-MEMBER TEAM: Member 4 =====
            // CHAPTER 6: Other School Campus Overview
            id: 'unc-campus',
            title: 'UNC Campus Overview',
            description: 'University of North Carolina at Chapel Hill. Three key locations emerge from student discussions.',
            image: './images/quad.jpg',
            duration: 2500,
            
            camera: {
                latitude: 35.9049,
                longitude: -79.0469,
                zoom: 14
            },
            
            showData: 'non_jmu_locations'    // Show only UNC locations
        },
        
        {
            // ===== 4-MEMBER TEAM: Member 4 | 5-MEMBER TEAM: Member 4 =====
            // CHAPTER 7: Other School Location 1
            id: 'unc-location-1',
            title: 'UNC Location 1: [Name Here]',
            description: 'Add your description here.',
            image: './images/d_hall.jpg',
            duration: 2000,
            
            camera: {
                latitude: 35.9050,
                longitude: -79.0470,
                zoom: 17
            },
            
            location: {
                name: 'UNC Location 1',
                latitude: 35.9050,
                longitude: -79.0470,
                postCount: 60,
                robertaScore: 0.30,
                isJMU: false                 // UNC location
            },
            
            showData: 'individual'
        },
        
        {
            // ===== 4-MEMBER TEAM: Member 4 | 5-MEMBER TEAM: Member 5 =====
            // CHAPTER 8: Other School Location 2
            id: 'unc-location-2',
            title: 'UNC Location 2: [Name Here]',
            description: 'Add your description here.',
            image: './images/arboretum.jpg',
            duration: 2000,
            
            camera: {
                latitude: 35.9060,
                longitude: -79.0480,
                zoom: 17
            },
            
            location: {
                name: 'UNC Location 2',
                latitude: 35.9060,
                longitude: -79.0480,
                postCount: 85,
                robertaScore: -0.10,
                isJMU: false
            },
            
            showData: 'individual'
        },
        
        {
            // ===== 4-MEMBER TEAM: Member 4 | 5-MEMBER TEAM: Member 5 =====
            // CHAPTER 9: Other School Location 3
            id: 'unc-location-3',
            title: 'UNC Location 3: [Name Here]',
            description: 'Add your description here.',
            image: './images/art_gallery.jpg',
            duration: 2000,
            
            camera: {
                latitude: 35.9070,
                longitude: -79.0490,
                zoom: 17
            },
            
            location: {
                name: 'UNC Location 3',
                latitude: 35.9070,
                longitude: -79.0490,
                postCount: 95,
                robertaScore: 0.40,
                isJMU: false
            },
            
            showData: 'individual'
        },
        {
            // ===== ALL TEAM SIZES: Member 1 =====
            // CHAPTER 10: Final zoom out
            id: 'conclusion',
            title: 'Conclusion: Comparing Campus Sentiment',
            description: 'Our analysis reveals both similarities and differences in how students experience and discuss these two universities.',
            image: './images/quad.jpg',
            duration: 3000,
            
            camera: {
                latitude: 37.2,
                longitude: -78.0,
                zoom: 8
            },
            
            showData: 'all_locations'
        }
    ]
};
