import Image from 'next/image';
import Link from 'next/link';
import Script from 'next/script';
import { Metadata } from 'next';
import styles from './page.module.css';

export const metadata: Metadata = {
  title: 'PitchPanel',
  description: 'Get instant singing feedback on pitch, breath, and diction with PitchPanel’s AI-powered analysis.',
  keywords: ['pitchpanel', 'vocal coach', 'singing feedback', 'ai music'],
  openGraph: {
    title: 'PitchPanel – AI Vocal Coach',
    description: 'Get instant singing feedback online.',
    url: 'https://pitchpanel.org',
    siteName: 'PitchPanel',
    images: [{ url: 'https://pitchpanel.org/public/logo.png', width: 1200, height: 630 }],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'PitchPanel',
    description: 'Get instant singing feedback with AI.',
    images: ['https://pitchpanel.org/og-image.png'],
  },
  robots: { index: true, follow: true },
};

export default function HomePage() {
  return (
      <>
        <Script
            id="json-ld"
            type="application/ld+json"
            dangerouslySetInnerHTML={{
              __html: JSON.stringify({
                '@context': 'https://schema.org',
                '@type': 'SoftwareApplication',
                name: 'PitchPanel',
                url: 'https://pitchpanel.org',
                description:
                    'PitchPanel is an AI vocal coach that provides feedback on pitch, breath, and diction.',
                applicationCategory: 'Music',
                operatingSystem: 'Web',
              }),
            }}
        />
        <main className={styles.container}>
          <div className={styles.bgGlow} />
          <section className={styles.heroSection}>
            <div className={styles.heroContent}>
              <h1 className={styles.heroTitle}>Master Your Voice with AI</h1>
              <p className={styles.heroSubtitle}>
                Real-time feedback. Smarter singing. Built for every vocalist.
              </p>
              <Link href="/product" className={styles.ctaButton}>
                Try PitchPanel
              </Link>
            </div>
            <div className={styles.heroImageContainer}>
              <Image
                  src="/analyzerScreenshot.png"
                  alt="PitchPanel product screenshot showing an audio analysis"
                  width={1200}
                  height={700}
                  className={styles.mockupImage}
                  priority
              />
            </div>
          </section>
          <section className={styles.featuresSection}>
            <div className={styles.featureItem}>
              <div className={styles.featureVisual} />
              <div className={styles.featureCard}>
                <h3 className={styles.featureTitle}>Instant Feedback</h3>
                <p className={styles.featureDescription}>
                  Get immediate insights on your pitch, breath, and diction as you sing.
                </p>
              </div>
            </div>
            <div className={styles.featureItem}>
              <div className={styles.featureCard}>
                <h3 className={styles.featureTitle}>AI-Powered Analysis</h3>
                <p className={styles.featureDescription}>
                  Our machine learning models provide a precise, objective score for your vocals.
                </p>
              </div>
              <div className={styles.featureVisual} />
            </div>
            <div className={styles.featureItem}>
              <div className={styles.featureVisual} />
              <div className={styles.featureCard}>
                <h3 className={styles.featureTitle}>Personalized Progress</h3>
                <p className={styles.featureDescription}>
                  Track your improvement over time with detailed performance metrics.
                </p>
              </div>
            </div>
          </section>
        </main>
      </>
  );
}