# jjshay.com

A personal portfolio and AI insights platform for John (JJ) Shay - AI Strategist & M&A Executive.

## Philosophy

**Concise. Minimalistic. Packed with subtle features.**

This single-page website delivers maximum value with minimal friction. Every element serves a purpose - from shareable LinkedIn recommendations to downloadable AI reports.

## Features

- **Animated Intro** - Subtle gold pulse with typewriter effect tagline
- **LinkedIn Recommendations Carousel** - Auto-scrolling testimonials with hover popups showing recommender details and direct LinkedIn profile links
- **Shareable Content** - Briefings and full reports designed for easy sharing and distribution
- **PDF Preview Modal** - In-browser document viewing with download options
- **Responsive Design** - Mobile-first approach, optimized for all devices
- **Hover Interactions** - Company/school logos enlarge and highlight on hover
- **Pure CSS Popups** - No JavaScript dependencies for recommendation popups

## Design System

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Deep Navy | `#0a1628` | Primary background |
| Navy | `#1a2d4a` | Secondary background, gradients |
| Gold | `#D4AF37` | Primary accent, headings, borders |
| Bright Gold | `#F4CF47` | Hover states, highlights |
| White | `#ffffff` | Body text |
| LinkedIn Blue | `#0077B5` | LinkedIn elements |

### Typography

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
```

- **Headings**: Inter Bold/Semi-Bold, Gold (#D4AF37)
- **Body**: Inter Regular, White with 85% opacity
- **Captions**: Inter, 11-14px, White with 50-60% opacity

### Visual Effects

- Radial gradient overlays with gold tones
- Glassmorphism cards with subtle gold borders
- Box shadows with gold glow on hover
- Smooth transitions (0.2-0.3s ease)

## Tech Stack

- **HTML5** - Semantic markup
- **CSS3** - Custom properties, flexbox, grid, animations
- **Vanilla JavaScript** - Minimal, for intro animation and PDF modal
- **No frameworks** - Zero dependencies, fast load times

## File Structure

```
jjshay.com/
├── index.html      # Single-page application
├── logo.png        # Site logo (gold on transparent)
├── og-image.png    # Social sharing preview image
├── playbook.png    # AI Acquisition Playbook cover
├── 46-55.png       # LinkedIn recommender headshots
└── README.md
```

## Performance

- Single HTML file with embedded CSS/JS
- External images loaded from CDN where possible
- Optimized for fast initial paint
- No render-blocking resources

## Deployment

Hosted on Namecheap via cPanel file manager. Simply upload `index.html` and assets to `public_html`.

## License

All rights reserved. This is a personal portfolio site.

---

*Built with attention to detail and a focus on providing value to the audience.*
