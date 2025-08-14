'use client';

import Image from 'next/image';
import styles from './about.module.css';

export default function AboutPage() {
  return (
      <div className={styles.aboutPage}>
        <main className={styles.container}>
          {/* Hero Section */}
          <section className={styles.hero}>
            <div className={styles.heroInner}>
              <h1 className={styles.heroTitle}>PitchPanel: Reinventing Vocal Mastery</h1>
              <p className={styles.heroSubtitle}>
                From bedrooms to Broadway — empowering voices through technology, accessibility, and innovation.
              </p>
            </div>
            <Image
                src="https://singersroom.com/wp-content/uploads/2023/11/15-Best-Male-Singers-of-All-Time.jpg"
                alt="Singer using PitchPanel"
                width={960}
                height={480}
                className={styles.heroImage}
            />
          </section>

          {/* Mission Cards Section */}
          <section className={styles.cardSection}>
            <h2 className={styles.sectionTitle}>Our Mission</h2>
            <div className={styles.cardGrid}>
              <div className={styles.card}>
                <h3>Accessible to All</h3>
                <p>
                  We believe vocal training shouldn't depend on geography or wealth. PitchPanel bridges gaps with inclusive tools.
                </p>
              </div>
              <div className={styles.card}>
                <h3>Feedback that Empowers</h3>
                <p>
                  Our AI gives real-time, friendly guidance that inspires consistent, effective practice between formal lessons.
                </p>
              </div>
              <div className={styles.card}>
                <h3>Innovation Meets Intuition</h3>
                <p>
                  Powerful technology should feel simple. Our interface is intuitive for beginners, and powerful for pros.
                </p>
              </div>
            </div>
          </section>

          {/* Origin Story Section */}
          <section className={styles.storySection}>
            <div className={styles.storyGrid}>
              <Image
                  src="https://antares-wp-media.sfo2.digitaloceanspaces.com/wp-content/uploads/20221212223752/home-recording-sound-like-professional-studio-04-1024x683.webp"
                  alt="Singer recording at home"
                  width={1000}
                  height={400}
                  className={styles.storyImage}
              />
              <div className={styles.storyText}>
                <h2 className={styles.sectionTitle}>Why We Built This</h2>
                <p>
                  Vocal training often comes with high barriers: expensive lessons, sparse feedback, intimidating environments.
                  Our founders — a music educator, a machine learning engineer, and a voice actor — knew there had to be a better way.
                </p>
                <p>
                  PitchPanel was born to bring expert guidance to anyone, anytime. Our goal: make vocal growth feel natural, supported, and possible — for every singer, everywhere.
                </p>
              </div>
            </div>
          </section>

          {/* Core Values Section */}
          <section className={styles.valuesSection}>
            <h2 className={styles.sectionTitle}>Our Core Values</h2>
            <div className={styles.valuesGrid}>
              <div className={styles.valueCard}>
                <h3>Equity</h3>
                <p>
                  Talent is everywhere. Opportunity isn't. We're here to change that through fair access and inclusive design.
                </p>
              </div>
              <div className={styles.valueCard}>
                <h3>Transparency</h3>
                <p>
                  No jargon, no gatekeeping. We explain how our tools work, so you always feel in control of your progress.
                </p>
              </div>
              <div className={styles.valueCard}>
                <h3>Community</h3>
                <p>
                  We don't just build tools — we foster a global space where singers lift each other up.
                </p>
              </div>
              <div className={styles.valueCard}>
                <h3>Creativity</h3>
                <p>
                  Your voice is your identity. We support artistry, not just accuracy.
                </p>
              </div>
            </div>
          </section>

          {/* Vision Section */}
          <section className={styles.visionSection}>
            <h2 className={styles.sectionTitle}>Our Vision</h2>
            <p className={styles.visionText}>
              We're not just building software — we're shaping the future of vocal education. One where AI enhances, not replaces, human artistry.
              One where singers are empowered, not overwhelmed. Our goal? A world where every voice has a chance to shine.
            </p>
          </section>

          {/* Call to Action */}
          <section className={styles.ctaSection}>
            <h2 className={styles.ctaTitle}>Are You Ready to Be Heard?</h2>
            <p className={styles.ctaSubtitle}>
              Join thousands of singers discovering their true sound. Start your PitchPanel journey today.
            </p>
          </section>
        </main>
      </div>
  );
}
