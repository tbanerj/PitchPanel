'use client';

import Image from 'next/image';
import styles from './page.module.css';
import Link from 'next/link';

export default function HomePage() {
  return (
    <main className={styles.container}>

      {/* Title Section */}
      <section className={styles.titleSection}>
        <h1 className={styles.title}>What is PitchPanel?</h1>
        <p className={styles.subtitle}>
          PitchPanel is your personal AI voice coach — a simple, web-based tool that gives singers instant feedback on their pitch, breath support, and diction.
        </p>
      </section>

      {/* Screenshot Image */}
      <section className={styles.imageSection}>
        <Image
          src="/analyzerScreenshot.png" // Replace with actual path to product screenshot
          alt="PitchPanel Product Screenshot"
          width={800}
          height={450}
          className={styles.image}
        />
      </section>

      {/* Summary Sentence */}
      <section className={styles.summarySection}>
        <p className={styles.summary}>
          It combines real-time vocal analysis, ML-based scoring, and personalized feedback into a lightweight web app.
        </p>
      </section>

      {/* Product Link */}
      <section className={styles.linkSection}>
        <Link href="/product">
          <button className={styles.learnMoreButton}>Try PitchPanel</button>
        </Link>
      </section>

    </main>
  );
}
