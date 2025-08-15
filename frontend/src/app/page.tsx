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
          <div className={styles.bgGlow}/>
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
            <div className={styles.glowContainer}>
              <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={styles.icon}
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="white"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
              >
                <path d="M9 18V5l12-2v13"/>
                <circle cx="6" cy="18" r="3"/>
                <circle cx="18" cy="16" r="3"/>
              </svg>
            </div>

            {/* Second Glow Container with elegant 8th note */}
            {/* Second Glow Container with properly positioned 8th note */}
            {/* Second Glow Container with classic 8th note */}
            {/* Second Glow Container with simple music note */}
            {/* Second Glow Container with a whole rest */}
            {/* Second Glow Container with filled whole rest */}
            {/* Second Glow Container with proper whole rest */}
            {/* Second Glow Container with larger whole rest */}
            <div className={styles.secondGlowContainer}>
              <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={styles.icon}
                  viewBox="0 0 24 24"
                  fill="white"
                  stroke="none"
              >
                {/* Main body of whole rest */}
                <rect x="7" y="9" width="10" height="8" rx="1" ry="1"/>

                {/* Extended top hat */}
                <rect x="5" y="7" width="14" height="3" rx="1" ry="1"/>
              </svg>
            </div>

            {/* Third Glow Container with whole rest */}
            {/* Third Glow Container with treble clef */}
            {/* Third Glow Container with proper treble clef */}
            {/* Third Glow Container with accurate treble clef */}
            {/* Third Glow Container with simple music note */}
            {/* Third Glow Container with clean eighth note */}
            {/* Third Glow Container with fully scaled, centered eighth note */}
            {/* Third Glow Container with fully scaled, centered eighth note */}
            {/* Third Glow Container with perfectly centered, scaled eighth note */}
            <div className={styles.thirdGlowContainer}>
              <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={styles.icon}
                  viewBox="0 0 32 32"  /* larger viewBox to avoid clipping */
                  fill="white"
                  stroke="none"
              >
                {/* Group for scaling and precise centering */}
                <g transform="translate(-5,0) scale(1.2)">
                  <circle cx="16" cy="20" r="4"/>
                  {/* note head */}
                  <rect x="18" y="4" width="2" height="16"/>
                  {/* stem */}
                  <path d="M20 4c0 0 6 1 2 6" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                  {/* flag */}
                </g>
              </svg>
            </div>
            {/*<div className={styles.audioSymbol}>*/}
            {/*  <div className={styles.audioArcOne}></div>*/}
            {/*  <div className={styles.audioArcTwo}></div>*/}
            {/*  <div className={styles.audioBody}></div>*/}
            {/*</div>*/}

            {/* Fourth Glow Container (mirrored glowContainer with same SVG) */}
            <div className={styles.fourthGlowContainer}>
              <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={styles.icon}
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="white"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
              >
                <path d="M9 18V5l12-2v13"/>
                <circle cx="6" cy="18" r="3"/>
                <circle cx="18" cy="16" r="3"/>
              </svg>
            </div>

            {/* Fifth Glow Container (mirrored secondGlowContainer with same SVG) */}
            <div className={styles.fifthGlowContainer}>
              <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={styles.icon}
                  viewBox="0 0 24 24"
                  fill="white"
                  stroke="none"
              >
                {/* Main body of whole rest */}
                <rect x="7" y="9" width="10" height="8" rx="1" ry="1"/>

                {/* Extended top hat */}
                <rect x="5" y="7" width="14" height="3" rx="1" ry="1"/>
              </svg>
            </div>

            {/* Sixth Glow Container (mirrored thirdGlowContainer with same SVG) */}
            <div className={styles.sixthGlowContainer}>
              <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={styles.icon}
                  viewBox="0 0 32 32"  /* larger viewBox to avoid clipping */
                  fill="white"
                  stroke="none"
              >
                <g transform="translate(-5,0) scale(1.2)">
                  <circle cx="16" cy="20" r="4"/>
                  {/* note head */}
                  <rect x="18" y="4" width="2" height="16"/>
                  {/* stem */}
                  <path d="M20 4c0 0 6 1 2 6" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                  {/* flag */}
                </g>
              </svg>
            </div>
            {/* Seventh Glow Container with microphone */}
            <div id="mic" className={styles.seventhGlowContainer}>
              <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={styles.icon}
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="white"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
              >
                {/* Microphone body */}
                <rect x="10" y="2" width="4" height="14" rx="2" ry="2"/>
                {/* Microphone base */}
                <line x1="12" y1="16" x2="12" y2="22"/>
                {/* Stand */}
                <line x1="8" y1="22" x2="16" y2="22"/>
              </svg>
            </div>
            {/* Futuristic chain links */}
            {/* Chains Container */}
            {/*<div className={styles.chainsContainer}>*/}
            {/*  {Array.from({ length: 6 }).map((_, i) => (*/}
            {/*      <svg*/}
            {/*          key={i}*/}
            {/*          className={`${styles.chain} ${styles[`chain${i + 1}`]}`}*/}
            {/*          viewBox="0 0 100 50"*/}
            {/*          preserveAspectRatio="none"*/}
            {/*      >*/}
            {/*        <path*/}
            {/*            d="M0,0 Q50,20 100,0"*/}
            {/*            stroke="white"*/}
            {/*            strokeWidth="3"*/}
            {/*            fill="none"*/}
            {/*            strokeLinecap="round"*/}
            {/*            strokeLinejoin="round"*/}
            {/*        />*/}

            {/*      </svg>*/}

            {/*  ))}*/}
            {/*</div>*/}
          </section>
  {/*do not touch a single line up here or the footer everything u need is below*/}


          {/*all this here is yours to work with go as much as u can fill as much space as possible*/}




          











































































































































          {/*stop here*/}

          <footer className={styles.footer}>
            <div className={styles.footerContainer}>
              <div className={styles.footerBrand}>
                <h2>PitchPanel</h2>
                <p>Your AI-powered vocal coach.</p>
              </div>
              <div className={styles.footerLinks}>
                <div>
                  <h3>Product</h3>
                  <Link href="/product">Features</Link>
                  <Link href="/pricing">Pricing</Link>
                  <Link href="/download">Download</Link>
                </div>
                <div>
                  <h3>Company</h3>
                  <Link href="/about">About</Link>
                  <Link href="/blog">Blog</Link>
                  <Link href="/careers">Careers</Link>
                </div>
                <div>
                  <h3>Support</h3>
                  <Link href="/help">Help Center</Link>
                  <Link href="/contact">Contact</Link>
                  <Link href="/faq">FAQ</Link>
                </div>
              </div>
              <div className={styles.footerBottom}>
                <p>© {new Date().getFullYear()} PitchPanel. All rights reserved.</p>
              </div>
            </div>
          </footer>
        </main>
      </>
  );
}