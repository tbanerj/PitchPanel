
import Image from 'next/image';
import styles from './page.module.css';
import Link from 'next/link';
import { Metadata } from 'next';
import Script from 'next/script';


export const metadata: Metadata = {
  title: 'PitchPanel',
  description: 'Get instant singing feedback on pitch, breath, and diction with PitchPanel’s AI-powered analysis.',
  keywords: ['pitchpanel', 'vocal coach', 'singing feedback', 'ai music'],
  openGraph: {
    title: 'PitchPanel – AI Vocal Coach',
    description: 'Get instant singing feedback online.',
    url: 'https://pitchpanel.org',
    siteName: 'PitchPanel',
    images: [
      {
        url: 'https://pitchpanel.org/public/logo.png',
        width: 1200,
        height: 630,
      },
    ],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'PitchPanel',
    description: 'Get instant singing feedback with AI.',
    images: ['https://pitchpanel.org/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
  },
};


export default function HomePage() {
  return (
      <>
        <Script
            id="json-ld"
            type="application/ld+json"
            dangerouslySetInnerHTML={{
              __html: JSON.stringify({
                "@context": "https://schema.org",
                "@type": "SoftwareApplication",
                name: "PitchPanel",
                url: "https://pitchpanel.org",
                description:
                    "PitchPanel is an AI vocal coach that provides feedback on pitch, breath, and diction.",
                applicationCategory: "Music",
                operatingSystem: "Web",
              }),
            }}
        />

        <main className={styles.container}>

          <section className={styles.heroBanner}>
            <Image
                src="/img1.jpg"
                alt="Colorful audio wave"
                fill
                className={styles.heroImage}
                priority
            />
            <div className={styles.heroOverlay}>
              <h1 className={styles.heroTitle}>Master Your Voice with AI</h1>
              <p className={styles.heroSubtitle}>
                Real-time feedback. Smarter singing. Built for every vocalist.
              </p>
            </div>
          </section>


          <section className={styles.titleSection}>
            <h1 className={styles.title}>What is PitchPanel?</h1>
            <p className={styles.subtitle}>
              PitchPanel is your personal AI voice coach — a simple, web-based tool that gives singers instant feedback
              on their pitch, breath support, and diction.
            </p>
          </section>

          <section className={styles.imageSection}>
            <Image
                src="/analyzerScreenshot.png"
                alt="PitchPanel Product Screenshot"
                width={800}
                height={450}
                className={styles.image}
            />
          </section>

          <section className={styles.summarySection}>
            <p className={styles.summary}>
              It combines real-time vocal analysis, ML-based scoring, and personalized feedback into a lightweight web
              app.
            </p>
          </section>

          <section className={styles.linkSection}>
            <Link href="/product">
              <button className={styles.learnMoreButton}>Try PitchPanel</button>
            </Link>
          </section>

        </main>

      </>

  );
}
