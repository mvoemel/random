import nodemailer from "nodemailer";

/**
 * This function sends an Email. It creates a transporter object and closes it
 * at the end. This approach is useful if you do not sent Email to often.
 *
 * @param {String} from defines from which Email addresse the email should be sent
 * @param {String} to defines to which Email addresse the email should be sent
 * @param {String} subject defines the subject with which the email should be sent
 * @param {String} text defines the text message with which the email should be sent
 */
const sendMail = ({ from, to, subject, text }) => {
  // Create SMTP transporter
  const transporter = nodemailer.createTransport({
    host: "smtp.youremail.com",
    port: 123,
    auth: {
      user: "yourname@yourremail.com",
      pass: "yourpassword",
    },
  });

  // Create MailOptions object with data that should be sent
  const mailOptions = { from, to, subject, text };

  // Send mail
  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error(error);
    } else {
      console.log("Email sent: " + info.response);
    }
  });

  // Close connection
  transporter.close();
};

export { sendMail };
