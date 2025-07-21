'use client';

import Image from 'next/image';
import styles from './team.module.css';

const teamMembers = [
  {
    name: 'Trinav Banerjee - Founder & CEO',
    image: '/people/trinav.jpeg',
    description: 'Seattle, WA',
  },
  {
    name: 'Alyssa Dhanji - Business/Marketing Team',
    image: '/people/alyssa.png',
    description: 'Toronto, Canada',
  },
  {
    name: 'Anna Zhang - Business/Marketing Team',
    image: '/people/anna.png',
    description: 'Toronto, Canada',
  },
  {
    name: 'Nikolay Li - Development Team',
    image: '/people/nikolay.png',
    description: 'Seattle, WA',
  },
  // {
  //   name: 'Saurish Srivastava - Development Team',
  //   image: '/fruit-2.jpg',
  //   description: 'Seattle, WA',
  // },
  {
    name: 'Aarav Kumar - Development Team',
    image: '/people/aarav.png',
    description: 'Seattle, WA',
  },
];

export default function TeamPage() {
  return (
    <main className={styles.container}>
      {/* Clean header section */}
      <section className={styles.header}>
        <h1 className={styles.heroTitle}>Our Team</h1>
        <p className={styles.heroSubtitle}>The group of people making it happen</p>
        <div className={styles.buttons}>
          <a href="https://www.instagram.com/pitchpanel/" target="_blank" rel="noopener noreferrer" className={styles.primaryButton}>
            Instagram
          </a>
          <a href="https://www.linkedin.com/company/pitchpanel" target="_blank" rel="noopener noreferrer" className={styles.secondaryButton}>
            LinkedIn
          </a>
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
            </div>
          </div>
        ))}
      </section>
    </main>
  );
}
