// ConvertKit Integration for Exit Popup
// Replace YOUR_FORM_ID with your actual ConvertKit form ID

async function submitToConvertKit(email) {
  const FORM_ID = 'YOUR_FORM_ID'; // Get this from ConvertKit settings
  
  try {
    const response = await fetch(`https://api.convertkit.com/v3/forms/${FORM_ID}/subscribe`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        tags: [5588443] // Optional: tag for "exit-popup-signup"
      })
    });
    
    if (response.ok) {
      console.log('✅ Email captured:', email);
      return true;
    } else {
      console.error('❌ ConvertKit error:', await response.text());
      return false;
    }
  } catch (error) {
    console.error('❌ Network error:', error);
    return false;
  }
}

// Update the form submission in base.html to call this:
// await submitToConvertKit(email);
