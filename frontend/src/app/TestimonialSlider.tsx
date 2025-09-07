

"use client";

import React, { useState } from 'react';
import styles from './page.module.css';


const testimonials = [
    {
        quote: "It is clear a lot of dedication and thought went into the production of PitchPanel. The team was incredibly receptive to feedback, and implemented said feedback into PitchPanel quickly and efficiently. This app offers advice that beginning singers may find helpful and encouraging!",
        author: "DJ Jordan, Seattle Voice Teacher"
    },
    {
        quote: "yoooo ts is sooo sick",
        author: "Aarav Kumar"
    },
    {
        quote: "Im saurish",
        author: "Saurish Srivastava",
    },
    {
        quote: "can i containerize now",
        author: "Nikolay Li",
    },
];

const TestimonialSlider = () => {
    const [currentIndex, setCurrentIndex] = useState(0);



    const goToPrevious = () => {
        const isFirstSlide = currentIndex === 0;
        const newIndex = isFirstSlide ? testimonials.length - 1 : currentIndex - 1;
        setCurrentIndex(newIndex);
    };

    const goToNext = () => {
        const isLastSlide = currentIndex === testimonials.length - 1;
        const newIndex = isLastSlide ? 0 : currentIndex + 1;
        setCurrentIndex(newIndex);
    };

    const goToSlide = (slideIndex: number) => {
        setCurrentIndex(slideIndex);
    };

    const currentTestimonial = testimonials[currentIndex];

    return (
        <section className={styles.testimonialSection}>
            <h2 className={styles.testimonialSubheading}>
                Here's what experts say:
            </h2>

            {/* Arrow Buttons */}
            <button onClick={goToPrevious} className={`${styles.sliderArrow} ${styles.arrowLeft}`}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
            </button>
            <button onClick={goToNext} className={`${styles.sliderArrow} ${styles.arrowRight}`}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 18l6-6-6-6"/></svg>
            </button>

            <div key={currentIndex} className={styles.testimonialContent}>
                <blockquote className={styles.testimonialQuote}>
                    “{currentTestimonial.quote}”
                </blockquote>
                <footer className={styles.testimonialAuthor}>
                    — {currentTestimonial.author}
                </footer>
            </div>

            {/* Indicator Dots */}
            <div className={styles.dotsContainer}>
                {testimonials.map((testimonial, slideIndex) => (
                    <button
                        key={slideIndex}
                        onClick={() => goToSlide(slideIndex)}
                        className={`${styles.dot} ${currentIndex === slideIndex ? styles.dotActive : ''}`}
                        aria-label={`Go to slide ${slideIndex + 1}`}
                    />
                ))}
            </div>
        </section>
    );
};

export default TestimonialSlider;