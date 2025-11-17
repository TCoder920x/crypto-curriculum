/** Accessibility statement page */
import React from 'react';
import { Box, Typography, Paper, List, ListItem, ListItemText, Link } from '@mui/material';
import { useThemeMode } from '../contexts/ThemeContext';
import { GlassSurface } from '../components/common/GlassSurface';

export const AccessibilityPage: React.FC = () => {
  const { mode } = useThemeMode();

  return (
    <Box sx={{ p: { xs: 2, sm: 4 }, maxWidth: 1200, mx: 'auto' }}>
      <GlassSurface variant="card" sx={{ p: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 3 }}>
          Accessibility Statement
        </Typography>
        
        <Typography variant="body1" paragraph>
          Crypto Curriculum Platform is committed to ensuring digital accessibility for people with disabilities. 
          We are continually improving the user experience for everyone and applying the relevant accessibility standards.
        </Typography>

        <Typography variant="h5" component="h2" sx={{ mt: 4, mb: 2 }}>
          Accessibility Features
        </Typography>

        <List>
          <ListItem>
            <ListItemText
              primary="Keyboard Navigation"
              secondary="All interactive elements can be accessed using only a keyboard. Use Tab to navigate, Enter/Space to activate buttons, and Escape to close dialogs."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Screen Reader Support"
              secondary="All content is properly labeled with ARIA attributes and semantic HTML for screen reader compatibility."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Color Contrast"
              secondary="Text meets WCAG AA standards with a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Focus Indicators"
              secondary="All interactive elements have visible focus indicators to help users track their position on the page."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Touch Targets"
              secondary="All interactive elements meet the minimum 44x44px touch target size for mobile devices."
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="Responsive Design"
              secondary="The platform is fully responsive and works across all device sizes from mobile to desktop."
            />
          </ListItem>
        </List>

        <Typography variant="h5" component="h2" sx={{ mt: 4, mb: 2 }}>
          Standards Compliance
        </Typography>

        <Typography variant="body1" paragraph>
          We aim to conform to the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA standards. 
          This includes:
        </Typography>

        <List>
          <ListItem>
            <ListItemText primary="Perceivable: Information and UI components are presentable in ways users can perceive." />
          </ListItem>
          <ListItem>
            <ListItemText primary="Operable: UI components and navigation must be operable." />
          </ListItem>
          <ListItem>
            <ListItemText primary="Understandable: Information and UI operation must be understandable." />
          </ListItem>
          <ListItem>
            <ListItemText primary="Robust: Content must be robust enough to be interpreted by assistive technologies." />
          </ListItem>
        </List>

        <Typography variant="h5" component="h2" sx={{ mt: 4, mb: 2 }}>
          Known Issues
        </Typography>

        <Typography variant="body1" paragraph>
          We are aware that some parts of the platform may not be fully accessible. We are working to address these issues 
          and improve accessibility across the platform. If you encounter any accessibility barriers, please contact us.
        </Typography>

        <Typography variant="h5" component="h2" sx={{ mt: 4, mb: 2 }}>
          Feedback
        </Typography>

        <Typography variant="body1" paragraph>
          We welcome your feedback on the accessibility of Crypto Curriculum Platform. If you encounter accessibility barriers, 
          please contact us:
        </Typography>

        <Box sx={{ mt: 2 }}>
          <Typography variant="body1">
            Email: <Link href="mailto:support@cryptocurriculum.org">support@cryptocurriculum.org</Link>
          </Typography>
          <Typography variant="body1" sx={{ mt: 1 }}>
            We aim to respond to accessibility feedback within 5 business days.
          </Typography>
        </Box>

        <Typography variant="h5" component="h2" sx={{ mt: 4, mb: 2 }}>
          Last Updated
        </Typography>

        <Typography variant="body2" color="text.secondary">
          This accessibility statement was last updated on {new Date().toLocaleDateString()}.
        </Typography>
      </GlassSurface>
    </Box>
  );
};

