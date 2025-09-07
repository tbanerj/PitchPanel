import Image from 'next/image';
import Link from 'next/link';
import Script from 'next/script';
import { Metadata } from 'next';
import styles from './page.module.css';
import FadeOnScroll from './fadeonscroll';
import TestimonialSlider from './TestimonialSlider';


declare module "*.png";
const analyzerPng = "/analyzerScreenshot.png";


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

const data = [
  { id: 1, text: 'Rural areas.' },
  { id: 2, text: 'Those with language barriers and more.' },
  { id: 3, text: 'Remote locations and beyond.' },
  { id: 4, text: 'Anyone with a passion for singing.' },
];

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
          {/* This glow will appear in the bottom-right of Image 2 */}
          <div className={`${styles.globalConnectingGlow} ${styles.globalConnectingGlow1}`} />
          {/* This glow will appear in the top-left of Image 3 */}
          <div className={`${styles.globalConnectingGlow} ${styles.globalConnectingGlow2}`} />
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
              <svg xmlns="http://www.w3.org/2000/svg" className={styles.icon} viewBox="0 0 24 24" fill="none"
                   stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 18V5l12-2v13"/>
                <circle cx="6" cy="18" r="3"/>
                <circle cx="18" cy="16" r="3"/>
              </svg>
            </div>
            <div className={styles.secondGlowContainer}>
              <svg xmlns="http://www.w3.org/2000/svg" className={styles.icon} viewBox="0 0 24 24" fill="white"
                   stroke="none">
                <rect x="7" y="9" width="10" height="8" rx="1" ry="1"/>
                <rect x="5" y="7" width="14" height="3" rx="1" ry="1"/>
              </svg>
            </div>
            <div className={styles.thirdGlowContainer}>
              <svg xmlns="http://www.w3.org/2000/svg" className={styles.icon} viewBox="0 0 32 32" fill="white"
                   stroke="none">
                <g transform="translate(-5,0) scale(1.2)">
                  <circle cx="16" cy="20" r="4"/>
                  <rect x="18" y="4" width="2" height="16"/>
                  <path d="M20 4c0 0 6 1 2 6" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                </g>
              </svg>
            </div>
            <div className={styles.fourthGlowContainer}>
              <svg xmlns="http://www.w3.org/2000/svg" className={styles.icon} viewBox="0 0 24 24" fill="none"
                   stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 18V5l12-2v13"/>
                <circle cx="6" cy="18" r="3"/>
                <circle cx="18" cy="16" r="3"/>
              </svg>
            </div>
            <div className={styles.fifthGlowContainer}>
              <svg xmlns="http://www.w3.org/2000/svg" className={styles.icon} viewBox="0 0 24 24" fill="white"
                   stroke="none">
                <rect x="7" y="9" width="10" height="8" rx="1" ry="1"/>
                <rect x="5" y="7" width="14" height="3" rx="1" ry="1"/>
              </svg>
            </div>
            <div className={styles.sixthGlowContainer}>
              <svg xmlns="http://www.w3.org/2000/svg" className={styles.icon} viewBox="0 0 32 32" fill="white"
                   stroke="none">
                <g transform="translate(-5,0) scale(1.2)">
                  <circle cx="16" cy="20" r="4"/>
                  <rect x="18" y="4" width="2" height="16"/>
                  <path d="M20 4c0 0 6 1 2 6" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                </g>
              </svg>
            </div>
            <div id="mic" className={styles.seventhGlowContainer}>
              <svg xmlns="http://www.w3.org/2000/svg" className={styles.icon} viewBox="0 0 24 24" fill="none"
                   stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="10" y="2" width="4" height="14" rx="2" ry="2"/>
                <line x1="12" y1="16" x2="12" y2="22"/>
                <line x1="8" y1="22" x2="16" y2="22"/>
              </svg>
            </div>
          </section>


          {/* SECTION: What is PitchPanel */}
          <section className={styles.heroSection}>
            <div className={styles.heroContent}> {/* Added a div for better grouping */}
              <h1 className={styles.heroHead}>What is PitchPanel</h1>
              <p className={styles.heroAarav}>
                PitchPanel is your personal AI voice coach — a simple, web-based tool that gives singers instant
                feedback
                on their pitch, breath support, and diction.
              </p>
            </div>
            {/* Closing heroContent div */}
            <Image
                src={analyzerPng}
                alt="PitchPanel Product Screenshot"
                width={400}
                height={225}
                className={styles.image}
            />
          </section>


          <section className={styles.featureHighlightSection}>
            {/* The squares are wrapped in FadeOnScroll for a staggered animation, with positioning applied to the wrapper */}
            <FadeOnScroll delay={200} wrapperClassName={styles.square1}>
              <div className={styles.glassSquare}>
                {/* Icon: Microphone */}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"
                     strokeLinejoin="round">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                  <line x1="12" y1="19" x2="12" y2="23"></line>
                  <line x1="8" y1="23" x2="16" y2="23"></line>
                </svg>
              </div>
            </FadeOnScroll>

            <FadeOnScroll delay={200} wrapperClassName={styles.square2}>
              <div className={styles.glassSquare}>
                {/* Icon: Detailed Audio Wave */}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"
                     strokeLinejoin="round">
                  <path d="M2 12h3l3-7 4 14 3-7h5"/>
                </svg>
              </div>
            </FadeOnScroll>

            <FadeOnScroll delay={200} wrapperClassName={styles.square3}>
              <div className={styles.glassSquare}>
                {/* Icon: Sound Bars / Equalizer */}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"
                     strokeLinejoin="round">
                  <path d="M5 18V6M12 21V3M19 15V9"/>
                </svg>
              </div>
            </FadeOnScroll>

            <FadeOnScroll delay={200} wrapperClassName={styles.square4}>
              <div className={styles.glassSquare}>
                {/* Icon: Simple Heartbeat/Pitch Line */}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"
                     strokeLinejoin="round">
                  <path d="M3 12h2.5l2-8 3 16 3-16 2 8h2.5"/>
                </svg>
              </div>
            </FadeOnScroll>

            {/* This inner container holds the content AND clips the glows */}
            <div className={styles.sectionInnerContainer}>
              {/* Background Glows are INSIDE the inner container */}
              <div className={`${styles.featureHighlightGlow} ${styles.featureHighlightGlow1}`}/>
              <div className={`${styles.featureHighlightGlow} ${styles.featureHighlightGlow2}`}/>

              {/* All your animated text content also goes INSIDE */}
              <FadeOnScroll>
                <h3 className={styles.animatedHeading}>It's not just a tool</h3>
              </FadeOnScroll>

              <FadeOnScroll delay={100}>
                <p className={styles.animatedParagraph1}>
                  It's the future. PitchPanel solves a big problem of lack of accessibility and feedback, seen in:
                </p>
              </FadeOnScroll>

              <FadeOnScroll items={data}/>

              <FadeOnScroll delay={300}>
                <p className={styles.animatedParagraph2}>
                  PitchPanel innovates; and can offer standalone feedback for beginners, or supplemental feedback for
                  students between traditional lessons, accessible to all.
                </p>
              </FadeOnScroll>
            </div>
          </section>

          <TestimonialSlider />

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

