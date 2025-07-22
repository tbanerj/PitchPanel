'use client';

import Image from 'next/image';
import styles from './about.module.css';

export default function AboutPage() {
  return (
    <div className={styles.aboutPage}>
      <main className={styles.container}>
        <section className={styles.headerSection}>
          <h1 className={styles.title}>About Us</h1>
          <p className={styles.subtitle}>Our story, ideas and long term vision</p>
        </section>

        <section className={styles.storySection}>
          <h2 className={styles.sectionTitle}>Our Story</h2>
          <p className={styles.paragraph}>
        Vocal training should be accessible to everyone — but for many singers, it isn’t. Traditional voice lessons can be expensive, hard to access in rural areas, and difficult to fit into a busy schedule. Feedback often comes just once a week, leaving students unsure if they’re practicing correctly. And for beginners, knowing where to start can be overwhelming. We created PitchPanel to change that. PitchPanel is a digital vocal coaching assistant designed to break down barriers in music education. It gives singers instant, personalized feedback from home — no private teacher, expensive equipment, or musical background required. Our goal isn’t to replace voice teachers, but to support them by helping students make the most of their practice time between lessons. The tool is designed to be intuitive for beginners, yet powerful enough to support serious musicians. Whether you're just starting your journey or looking to sharpen your skills between lessons, PitchPanel gives you the clarity and encouragement to grow as a singer — on your terms.
          </p>
          <p className={styles.paragraph}>
            Our team brings together musicians, engineers, and educators passionate about expanding access to artistic tools. We believe that music education should be as flexible and adaptive as the people who pursue it.
          </p>
        </section>

        <section className={styles.imageGridSection}>
          <div className={styles.imageGrid}>
            
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
    </div>
  );
}
