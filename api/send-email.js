const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { to, subject, body, html } = req.body || {};

  if (!to || !subject || !body) {
    return res.status(400).json({ error: 'Missing required fields: to, subject, body' });
  }

  const EMAIL_USER = process.env.EMAIL_ADDRESS;
  const EMAIL_PASS = process.env.EMAIL_PASSWORD;

  if (!EMAIL_USER || !EMAIL_PASS) {
    console.error('EMAIL_ADDRESS or EMAIL_PASSWORD not configured in Vercel env');
    return res.status(500).json({ error: 'Server email configuration missing' });
  }

  const transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 465,
    secure: true,
    auth: {
      user: EMAIL_USER,
      pass: EMAIL_PASS,
    },
  });

  try {
    const info = await transporter.sendMail({
      from: `"Digicard Design" <${EMAIL_USER}>`,
      to,
      subject,
      text: body,
      ...(html ? { html } : {}),
    });

    console.log('Email sent:', info.messageId);
    return res.status(200).json({ success: true, messageId: info.messageId });
  } catch (err) {
    console.error('Email send failed:', err);
    return res.status(500).json({ error: 'Failed to send email', detail: err.message });
  }
};
