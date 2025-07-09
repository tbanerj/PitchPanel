'use client';

import Image from 'next/image';
import styles from './team.module.css';

const teamMembers = [
  {
    name: 'Trinav Banerjee - Founder & CEO',
    image: '/people/trinav.jpeg',
    description: 'Their info and the buttons link to their linkedin, insta or whatever.',
  },
  {
    name: 'Indrajit Banerjee - Advisor',
    image: '/fruit-2.jpg',
    description: 'Their info and the buttons link to their linkedin, insta or whatever.',
  },
  {
    name: 'Alyssa Dhanji - Business/Marketing Team',
    image: '/fruit-3.jpg',
    description: 'Their info and the buttons link to their linkedin, insta or whatever.',
  },
  {
    name: 'Anna Zhang - Business/Marketing Team',
    image: '/fruit-2.jpg',
    description: 'Their info and the buttons link to their linkedin, insta or whatever.',
  },
  {
    name: 'Nikolay Li - Development Team',
    image: '/fruit-3.jpg',
    description: 'Their info and the buttons link to their linkedin, insta or whatever.',
  },
  {
    name: 'Saurish Srivastava - Development Team',
    image: '/fruit-2.jpg',
    description: 'A subheading for this section, as long or as short as you like. Their info and the buttons link to their linkedin, insta or whatever.',
  },
  {
    name: 'Aarav Kumar - Development Team',
    image: '/fruit-3.jpg',
    description: 'Their info and the buttons link to their linkedin, insta or whatever.',
  },
];

export default function TeamPage() {
  return (
    <main className={styles.container}>
      <section className={styles.heroSection}>
        <Image
          src="/team-hero.jpg"
          alt="Team Banner"
          width={1200}
          height={400}
          className={styles.heroImage}
        />
        <div className={styles.heroOverlay}>
          <h1 className={styles.heroTitle}>Our Team</h1>
          <p className={styles.heroSubtitle}>The group of people making it happen</p>
          <a href="https://www.instagram.com/pitchpanel/" className={styles.heroButton}>Insta</a>
        </div>
      </section>

      <section className={styles.membersGrid}>
        {teamMembers.map((member, index) => (
          <div key={index} className={styles.memberCard}>
            <Image
              src={member.image}
              alt={member.name}
              width={300}
              height={300}
              className={styles.memberImage}
            />
            <div className={styles.memberInfo}>
              <h2>{member.name}</h2>
              <p>{member.description}</p>
              <div className={styles.buttons}>
                <button className={styles.primaryButton}>Button</button>
                <button className={styles.secondaryButton}>Secondary button</button>
              </div>
            </div>
          </div>
        ))}
      </section>
    </main>
  );
}
