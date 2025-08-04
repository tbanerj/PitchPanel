'use client';

import styles from './privacy.module.css';

export default function PrivacyPolicyPage() {
  return (
    <div className={styles.privacyPage}>
      <main className={styles.container}>
        <section className={styles.headerSection}>
          <h1 className={styles.title}>Privacy Policy</h1>
          <p className={styles.subtitle}>Your privacy matters — here's how we protect it</p>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Effective Date</h2>
          <p className={styles.paragraph}>August 4, 2025</p>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Our Commitment</h2>
          <p className={styles.paragraph}>
            At PitchPanel, your privacy is our priority. We do not collect, store, or share any personal information or audio recordings. PitchPanel is designed to be safe, secure, and respectful of your data.
          </p>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>What We Don’t Collect</h2>
          <ul className={styles.bulletList}>
            <li>No names, emails, or personal information</li>
            <li>No audio recordings are saved or stored</li>
            <li>No usage tracking or behavioral analytics</li>
            <li>No cookies for advertising or profiling</li>
          </ul>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>What We Do</h2>
          <ul className={styles.bulletList}>
            <li>Provide real-time vocal analysis using temporary input</li>
            <li>Immediately discard all data after analysis is complete</li>
            <li>Use secure, encrypted communication methods</li>
            <li>Maintain a private, anonymous, and ad-free experience</li>
          </ul>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Our Philosophy</h2>
          <p className={styles.paragraph}>
            PitchPanel was built to help you improve your singing without ever compromising your privacy. You stay in control. We do not store any part of your session, and we don’t use your data to track or target you.
          </p>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Contact Us</h2>
          <p className={styles.paragraph}>
            If you have any questions or concerns about privacy, reach out to us at: <strong>pitchpanel.team@gmail.com</strong>
          </p>
        </section>
      </main>
    </div>
  );
}
