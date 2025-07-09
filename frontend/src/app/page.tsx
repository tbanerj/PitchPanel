'use client';

import Image from 'next/image';
import styles from './page.module.css';

export default function HomePage() {
  return (
    <main className={styles.container}>


      {/* Title */}
      <section className={styles.titleSection}>
        <h1 className={styles.title}>Welcome to Pitch Panel!</h1>
        <p className={styles.subtitle}>The Next Generation of Vocal Training</p>
      </section>

      {/* Purpose Section */}
      <section className={styles.purposeSection}>
        <h2 className={styles.sectionHeader}>Purpose</h2>
        <div className={styles.purposeGrid}>
          <div className={styles.textColumn}>
            <div className={styles.card}>
              <h3>Problem</h3>
              <p>
                Despite the benefits of vocal training, quality vocal coaching remains out of reach
                for many people due to several key barriers
              </p>
            </div>
            <div className={styles.card}>
              <h3>Solution</h3>
              <p>
                PitchPanel is a digital vocal coaching assistant that provides:
              </p>
              <ul>
                <li>Standalone feedback for beginners, or</li>
                <li>Supplemental feedback for students between traditional lessons.</li>
              </ul>
              <p>
                It combines real-time vocal analysis, ML-based scoring, and personalized feedback
                into a lightweight web app.
              </p>
            </div>
            <div className={styles.card}>
              <h3>Mission statement</h3>
              <p className={styles.placeholder}>someone make a mission statement bro…</p>
            </div>
          </div>
          <div className={styles.imageColumn}>
            <Image
              src="/mic.png"
              alt="Microphone"
              width={600}
              height={400}
              className={styles.image}
            />
          </div>
        </div>
      </section>

      {/* Product Section */}
      <section className={styles.productSection}>
        <h2 className={styles.sectionHeader}>Product</h2>
        <Image
          src="/pitchpanel-croissant.jpg"
          alt="croissant with grapes"
          width={1000}
          height={500}
          className={styles.bannerImage}
        />
        <button className={styles.learnMoreButton}>Learn more</button>
      </section>
    </main>
  );
}
