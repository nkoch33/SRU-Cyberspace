// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Calendar Functionality
class Calendar {
    constructor() {
        this.currentDate = new Date();
        this.currentMonth = this.currentDate.getMonth();
        this.currentYear = this.currentDate.getFullYear();
        this.events = this.getSampleEvents();
        
        this.init();
    }

    init() {
        this.renderCalendar();
        this.bindEvents();
        this.updateEventList();
    }

    getSampleEvents() {
        return [
            {
                date: new Date(this.currentYear, this.currentMonth, 15),
                title: "Cybersecurity Capture the Flag",
                description: "Hands-on ethical hacking challenges and security puzzles."
            },
            {
                date: new Date(this.currentYear, this.currentMonth, 22),
                title: "Digital Forensics Workshop",
                description: "Learn evidence collection and analysis techniques."
            },
            {
                date: new Date(this.currentYear, this.currentMonth, 28),
                title: "Network Security Lab",
                description: "Practice penetration testing and defense strategies."
            },
            {
                date: new Date(this.currentYear, this.currentMonth + 1, 5),
                title: "Cybersecurity Career Panel",
                description: "Meet industry professionals from security firms and agencies."
            },
            {
                date: new Date(this.currentYear, this.currentMonth + 1, 12),
                title: "Incident Response Simulation",
                description: "Real-world scenario training for security incidents."
            }
        ];
    }

    renderCalendar() {
        const calendarDays = document.getElementById('calendarDays');
        const currentMonthElement = document.getElementById('currentMonth');
        
        // Update month display
        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        currentMonthElement.textContent = `${monthNames[this.currentMonth]} ${this.currentYear}`;
        
        // Clear previous calendar
        calendarDays.innerHTML = '';
        
        // Get first day of month and number of days
        const firstDay = new Date(this.currentYear, this.currentMonth, 1);
        const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0);
        const startDate = new Date(firstDay);
        startDate.setDate(startDate.getDate() - firstDay.getDay());
        
        // Generate calendar days
        for (let i = 0; i < 42; i++) {
            const date = new Date(startDate);
            date.setDate(startDate.getDate() + i);
            
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.textContent = date.getDate();
            
            // Check if it's today
            if (this.isToday(date)) {
                dayElement.classList.add('today');
            }
            
            // Check if it's current month
            if (date.getMonth() !== this.currentMonth) {
                dayElement.classList.add('other-month');
            }
            
            // Check if it has events
            if (this.hasEvents(date)) {
                dayElement.classList.add('has-event');
            }
            
            // Add click event for event details
            dayElement.addEventListener('click', () => this.showEventDetails(date));
            
            calendarDays.appendChild(dayElement);
        }
    }

    isToday(date) {
        const today = new Date();
        return date.getDate() === today.getDate() &&
               date.getMonth() === today.getMonth() &&
               date.getFullYear() === today.getFullYear();
    }

    hasEvents(date) {
        return this.events.some(event => 
            event.date.getDate() === date.getDate() &&
            event.date.getMonth() === date.getMonth() &&
            event.date.getFullYear() === date.getFullYear()
        );
    }

    showEventDetails(date) {
        const dayEvents = this.events.filter(event => 
            event.date.getDate() === date.getDate() &&
            event.date.getMonth() === date.getMonth() &&
            event.date.getFullYear() === date.getFullYear()
        );
        
        if (dayEvents.length > 0) {
            const eventDetails = dayEvents.map(event => 
                `${event.title}: ${event.description}`
            ).join('\n');
            
            alert(`Events on ${date.toLocaleDateString()}:\n\n${eventDetails}`);
        }
    }

    nextMonth() {
        this.currentMonth++;
        if (this.currentMonth > 11) {
            this.currentMonth = 0;
            this.currentYear++;
        }
        this.renderCalendar();
        this.updateEventList();
    }

    prevMonth() {
        this.currentMonth--;
        if (this.currentMonth < 0) {
            this.currentMonth = 11;
            this.currentYear--;
        }
        this.renderCalendar();
        this.updateEventList();
    }

    updateEventList() {
        const eventList = document.getElementById('eventList');
        const currentMonthEvents = this.events.filter(event => 
            event.date.getMonth() === this.currentMonth &&
            event.date.getFullYear() === this.currentYear
        );
        
        eventList.innerHTML = '';
        
        if (currentMonthEvents.length === 0) {
            eventList.innerHTML = '<p style="color: #6b7280; text-align: center;">No events this month</p>';
            return;
        }
        
        currentMonthEvents.forEach(event => {
            const eventElement = document.createElement('div');
            eventElement.className = 'event-item';
            eventElement.innerHTML = `
                <div class="event-date">${event.date.toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    month: 'short', 
                    day: 'numeric' 
                })}</div>
                <div class="event-title">${event.title}</div>
                <div class="event-description">${event.description}</div>
            `;
            eventList.appendChild(eventElement);
        });
    }

    bindEvents() {
        document.getElementById('nextMonth').addEventListener('click', () => this.nextMonth());
        document.getElementById('prevMonth').addEventListener('click', () => this.prevMonth());
    }
}

// Form Submission with Security
const joinForm = document.querySelector('.join-form');
if (joinForm) {
    joinForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const year = document.getElementById('year').value;
        
        if (name && email && year) {
            try {
                // Get CSRF token from hidden input
                const csrfToken = document.querySelector('input[name="csrf_token"]').value;
                
                // Prepare form data
                const formData = new FormData();
                formData.append('name', name);
                formData.append('email', email);
                formData.append('year', year);
                formData.append('csrf_token', csrfToken);
                
                // Submit form securely
                const response = await fetch('/submit-form', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const result = await response.json();
                
                if (response.ok && result.success) {
                    // Show success message
                    alert(result.message);
                    
                    // Reset form
                    this.reset();
                } else {
                    // Show error message
                    alert(result.error || 'An error occurred. Please try again.');
                }
                
            } catch (error) {
                console.error('Form submission error:', error);
                alert('An error occurred. Please try again.');
            }
        } else {
            alert('Please fill in all fields.');
        }
    });
}

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.mission-card, .resource-card, .sponsor-card');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});



// Add some interactive features
document.addEventListener('DOMContentLoaded', () => {
    // Add hover effects to floating cards
    const floatingCards = document.querySelectorAll('.floating-card');
    floatingCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-15px) scale(1.05)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add click effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
