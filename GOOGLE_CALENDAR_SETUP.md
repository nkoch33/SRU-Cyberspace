# Google Calendar Integration Setup

## Step 1: Get Your Google Calendar ID

1. Go to [Google Calendar](https://calendar.google.com)
2. Find your SRU Cyberspace Club calendar (or create one)
3. Click the three dots next to your calendar name → "Settings and sharing"
4. Scroll down to "Integrate calendar" section
5. Copy the "Calendar ID" (it looks like: `abc123@group.calendar.google.com`)

## Step 2: Update the HTML

Replace `YOUR_CALENDAR_ID_HERE` in the `index.html` file with your actual calendar ID:

```html
<iframe 
    src="https://calendar.google.com/calendar/embed?src=YOUR_ACTUAL_CALENDAR_ID&ctz=America%2FNew_York&mode=MONTH&showTitle=0&showNav=1&showDate=1&showPrint=0&showTabs=1&showCalendars=0&showTz=0"
    style="border: 0" 
    width="100%" 
    height="600" 
    frameborder="0" 
    scrolling="no">
</iframe>
```

## Step 3: Update the Mobile Link

Also update the mobile events link with your calendar ID:

```html
<p class="events-note">View our full calendar above or check out our <a href="https://calendar.google.com/calendar/embed?src=YOUR_ACTUAL_CALENDAR_ID" target="_blank">Google Calendar</a> for all events.</p>
```

## Step 4: Customize Calendar Display

You can modify the iframe URL parameters:

- `mode=MONTH` - Change to `WEEK` or `AGENDA` for different views
- `showTitle=0` - Set to `1` to show calendar title
- `showNav=1` - Set to `0` to hide navigation
- `showDate=1` - Set to `0` to hide date
- `ctz=America%2FNew_York` - Change timezone as needed

## Benefits of This Approach

✅ **Automatic Updates**: Events added to Google Calendar appear instantly on your website
✅ **Easy Management**: Manage events from Google Calendar app/website
✅ **Real-time Sync**: No need to manually update website when events change
✅ **Mobile Friendly**: Calendar works perfectly on all devices
✅ **Professional Look**: Clean, modern calendar interface
✅ **No Maintenance**: No JavaScript calendar code to maintain

## Alternative: Google Calendar API (Advanced)

If you want more control, you can use the Google Calendar API to:
- Display events in a custom format
- Filter events by date range
- Show only upcoming events
- Customize the styling completely

This requires setting up Google Cloud credentials and using JavaScript to fetch events.

## Troubleshooting

- **Calendar not showing**: Check that your calendar ID is correct and the calendar is public
- **Events not visible**: Ensure the calendar is shared publicly or with appropriate permissions
- **Styling issues**: The iframe inherits Google's styling, but you can customize the container
