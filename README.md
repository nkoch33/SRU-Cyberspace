
# Slippery Rock University Cyberspace Club Website

A modern, responsive website for the SRU Cyberspace Club with enhanced features including an interactive calendar for upcoming cybersecurity events and workshops.

## Features

### Core Features
- **Modern Design**: Clean, professional design for cybersecurity and digital innovation
- **Responsive Layout**: Fully responsive design that works on all devices
- **Interactive Calendar**: Monthly calendar view with cybersecurity event management
- **Smooth Animations**: Beautiful hover effects and scroll animations
- **Mobile Navigation**: Hamburger menu for mobile devices

### Sections
1. **Hero Section**: Eye-catching introduction with cybersecurity-focused floating cards
2. **Mission**: Clear statement of the club's cybersecurity and innovation purpose
3. **Events Calendar**: Interactive calendar showing upcoming cybersecurity events
4. **Resources**: Links to cybersecurity tools, forensics lab, and security blog
5. **Sponsors**: Recognition of cybersecurity industry sponsors
6. **Join Form**: Student registration form for the club
7. **Footer**: Contact information and social links

### Calendar Features
- Monthly navigation (previous/next month)
- Event indicators on calendar days
- Event list showing current month's cybersecurity highlights
- Click on dates to view event details
- Sample cybersecurity events included for demonstration

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox and Grid
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icons
- **Google Fonts**: Inter font family

## Project Structure

```
car_detection_project/
├── index.html          # Main HTML file
├── styles.css          # CSS styles
├── script.js           # JavaScript functionality
└── README.md           # Project documentation
```

## Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- No build tools or dependencies required

### Installation
1. Clone or download the project files
2. Open `index.html` in your web browser
3. The website will load with all functionality ready

### Local Development
For local development, you can use any local server:

```bash
# Using Python 3
python -m http.server 8000

# Using Node.js
npx serve .

# Using PHP
php -S localhost:8000
```

Then open `http://localhost:8000` in your browser.

## Customization

### Adding Events
To add new events, modify the `getSampleEvents()` method in `script.js`:

```javascript
getSampleEvents() {
    return [
        {
            date: new Date(2024, 11, 25), // December 25, 2024
            title: "Christmas Hackathon",
            description: "Holiday-themed coding challenge"
        },
        // Add more events here...
    ];
}
```

### Changing Colors
The main color scheme can be modified in `styles.css`:

```css
:root {
    --primary-color: #2563eb;      /* Blue */
    --accent-color: #fbbf24;       /* Yellow */
    --text-color: #1f2937;         /* Dark gray */
    --background-color: #f8fafc;   /* Light gray */
}
```

### Adding New Sections
To add new sections, follow the existing pattern in `index.html` and add corresponding styles in `styles.css`.

## Responsive Design

The website is fully responsive with breakpoints at:
- **Desktop**: 1200px and above
- **Tablet**: 768px - 1199px
- **Mobile**: Below 768px

## Key Features Explained

### Interactive Calendar
The calendar system includes:
- Month navigation
- Event highlighting
- Click-to-view event details
- Responsive grid layout

### Smooth Scrolling
Navigation links smoothly scroll to sections using:
```javascript
target.scrollIntoView({
    behavior: 'smooth',
    block: 'start'
});
```

### Intersection Observer
Elements animate in as they come into view:
```javascript
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
});
```

## Future Enhancements

Potential improvements for the future:
- **Event Management System**: Admin panel for adding/editing events
- **User Authentication**: Member login system
- **Event Registration**: RSVP functionality for events
- **Database Integration**: Store events and user data
- **Email Notifications**: Automated event reminders
- **Social Media Integration**: Share events on social platforms

## Contributing

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with modern web technologies
- Designed specifically for cybersecurity student organizations
- Tailored for Slippery Rock University's Cyberspace Club
- Heavily inspired by the University of Pittsburgh Computer Science Club
- Usage of generative AI to produce the README files

## Support

For questions or support, please open an issue in the project repository.

---

**Built with love for the SRU Cyberspace community**
