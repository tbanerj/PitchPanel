"use client";

import React, { useState, useEffect, useRef } from 'react'; // <-- TYPO IS FIXED HERE
import styles from './page.module.css';

interface Item {
    id: number;
    text: string;
}

interface FadeOnScrollProps {
    children?: React.ReactNode;
    items?: Item[];
    delay?: number;
    wrapperClassName?: string;
}

const FadeOnScroll: React.FC<FadeOnScrollProps> = ({ children, items, delay = 0, wrapperClassName = '' }) => {
    const [isVisible, setIsVisible] = useState(false);
    const domRef = useRef<HTMLDivElement | HTMLUListElement>(null);

    useEffect(() => {
        const currentRef = domRef.current;
        if (!currentRef) return;

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        setTimeout(() => {
                            setIsVisible(true);
                        }, delay);
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.2 }
        );

        observer.observe(currentRef);

        return () => {
            if (currentRef) {
                observer.unobserve(currentRef);
            }
        };
    }, [delay]);

    if (items) {
        return <AnimatedList items={items} />;
    }

    return (
        <div
            ref={domRef as React.RefObject<HTMLDivElement>}
            className={`${wrapperClassName} ${styles.fadeInElement} ${isVisible ? styles.fadeInElementVisible : ''}`}
        >
            {children}
        </div>
    );
};

// --- Helper component for the list ---
const AnimatedList: React.FC<{ items: Item[] }> = ({ items }) => {
    const [visibleItems, setVisibleItems] = useState<Set<number>>(new Set());
    const itemRefs = useRef<Map<number, HTMLLIElement | null>>(new Map());

    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    const id = Number(entry.target.getAttribute('data-id'));
                    if (entry.isIntersecting) {
                        setVisibleItems((prev) => new Set(prev).add(id));
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 }
        );

        const currentRefs = itemRefs.current;
        currentRefs.forEach((item) => {
            if (item) observer.observe(item);
        });

        return () => {
            currentRefs.forEach((item) => {
                if (item) observer.unobserve(item);
            });
        };
    }, [items]);

    return (
        <ul className={styles['list-container']}>
            {items.map((item, index) => (
                <li
                    key={item.id}
                    data-id={item.id}
                    ref={(node) => {
                        if (node) itemRefs.current.set(item.id, node);
                        else itemRefs.current.delete(item.id);
                    }}
                    style={{ transitionDelay: `${index * 100}ms` }}
                    className={`${styles['list-item']} ${visibleItems.has(item.id) ? styles['fade-in-visible'] : ''}`}
                >
                    {item.text}
                </li>
            ))}
        </ul>
    );
};

export default FadeOnScroll;