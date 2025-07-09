'use client';

import Image from 'next/image';
import styles from './about.module.css';

export default function AboutPage() {
  return (
    <main className={styles.container}>
      <section className={styles.headerSection}>
        <h1 className={styles.title}>About Us</h1>
        <p className={styles.subtitle}>Our story, ideas and long term vision</p>
      </section>

      <section className={styles.storySection}>
        <h2 className={styles.sectionTitle}>Our Story</h2>
        <p className={styles.paragraph}>
          PitchPanel began with a simple idea: to make high-quality vocal training accessible to anyone, anywhere.
          Drawing on innovations in music education, AI, and feedback technology, we created a lightweight platform that empowers users to grow vocally on their own terms.
        </p>
        <p className={styles.paragraph}>
          Our team brings together musicians, engineers, and educators passionate about expanding access to artistic tools. We believe that music education should be as flexible and adaptive as the people who pursue it.
        </p>
      </section>

      <section className={styles.imageGridSection}>
        <div className={styles.imageGrid}>
          <Image src="/fruit-bread.jpg" alt="bread and wine" width={600} height={400} className={styles.image} />
          <Image src="/apricots-bottle.jpg" alt="apricots and bottle" width={600} height={400} className={styles.image} />
        </div>
      </section>

      <section className={styles.textBlockSection}>
        <p className={styles.paragraph}>
          Today, we continue to evolve — refining our feedback engine, listening to users, and reimagining how coaching can work in digital spaces. Whether you’re an aspiring singer or a seasoned performer, we’re building the tools to help you grow.
        </p>
        <p className={styles.paragraph}>
          Our long-term vision is clear: personalized, scalable, and beautifully human musical support for anyone who wants to be heard.
        </p>
      </section>
    </main>
  );
}
