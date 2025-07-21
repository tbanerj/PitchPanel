'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import styles from './Navbar.module.css';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
      if (window.innerWidth > 768) {
        setIsOpen(false);
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const closeMenu = () => {
    if (isMobile) {
      setIsOpen(false);
    }
  };

  return (
    <nav className={styles.navbar}>
      <div className={styles.navContainer}>
        <div className={styles.navContent}>
          <div className={styles.logo}>
            <Link href="/" onClick={closeMenu}>Pitch Panel</Link>
          </div>

          <button
            className={`${styles.hamburger} ${isOpen ? styles.open : ''}`}
            onClick={() => setIsOpen(!isOpen)}
            aria-label="Toggle menu"
            aria-expanded={isOpen}
          >
            <span className={styles.bar}></span>
            <span className={styles.bar}></span>
            <span className={styles.bar}></span>
          </button>

          <div className={`${styles.navLinksContainer} ${isOpen ? styles.showMenu : ''}`}>
            <ul className={styles.navLinks}>
              <li><Link href="/" onClick={closeMenu}>Home</Link></li>
              <li><Link href="/product" onClick={closeMenu}>Product</Link></li>
              <li><Link href="/about" onClick={closeMenu}>About Us</Link></li>
              <li><Link href="/team" onClick={closeMenu}>Team</Link></li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;