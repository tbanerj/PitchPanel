"use client";

import React from "react";
import Link from "next/link";
import styles from "./Footer.module.css";

const Footer: React.FC = () => {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerContainer}>
        <div className={styles.footerBrand}>
          <h2>PitchPanel</h2>
          <p>Your AI-powered vocal coach.</p>
        </div>

        <div className={styles.footerLinks}>
          <div>
            <h3>Product</h3>
            <Link href="/product">Product</Link>
            {/* External link: open in new tab and add rel for security */}
            <Link
              href="https://apps.apple.com/us/app/pitchpanel/id6749473625"
              target="_blank"
              rel="noopener noreferrer"
            >
              Download
            </Link>
          </div>

          <div>
            <h3>Company</h3>
            <Link href="/about">About</Link>
            <Link href="/team">Team</Link>
          </div>

          <div>
            <h3>Support</h3>
            {/* For mailto, a plain <a> is slightly cleaner, but Link works too */}
            <a href="mailto:pitchpanel.team@gmail.com">Contact</a>
            <Link href="/privacy">Privacy Policy</Link>
          </div>
        </div>

        <div className={styles.footerBottom}>
          <p>© {new Date().getFullYear()} PitchPanel. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
