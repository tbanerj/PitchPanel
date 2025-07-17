<script lang="ts">
    import {onMount} from "svelte";

    onMount(() => {
        document.title = "Pitch Panel";
    })
</script>

<main class="relative w-full min-h-screen bg-bg">
    <div class="relative mx-auto w-fit text-center py-[7rem]">
        <header class="text-text text-7xl font-semibold">Pitch Panel</header>
        <h1 class="text-text-muted text-2xl">The future of music education</h1>
    </div>

    <section class="relative grid grid-cols-2 h-[80vh] mx-auto w-[70%] p-8 gap-4">
        <div class="w-full h-full space-y-2 grid grid-rows-12 overflow-hidden">

            <div class="row-span-2 w-full rounded-xl border-3 border-border bg-bg-light p-4 flex flex-col justify-center">
                <header class="font-semibold text-5xl">
                    Purpose
                </header>
            </div>

            <div class="row-span-3 w-full rounded-xl border-3 border-border bg-bg-light p-4 flex flex-col justify-center">
                <header class="font-semibold text-3xl">
                    Problem
                </header>
                <h1 class="2xl text-text-muted">
                    Despite the benefits of vocal training,
                    quality vocal coaching remains out of reach for many people due to several key barriers
                </h1>
            </div>

            <div class="row-span-4 w-full rounded-xl border-3 border-border bg-bg-light p-4 flex flex-col justify-center">
                <header class="font-semibold text-3xl">
                    Solution
                </header>
                <h1 class="2xl text-text-muted">
                    PitchPanel is a digital vocal coaching assistant that provides:
                </h1>
                <ul class="2xl text-text-muted list-disc list-inside">
                    <li>Standalone feedback for beginners</li>
                    <li>Supplemental feedback for students between traditional lessons.</li>
                </ul>
                <h1 class="2xl text-text-muted">
                    It combines real-time vocal analysis, ML-based scoring, and personalized feedback into a lightweight web app.
                </h1>
            </div>

            <div class="row-span-3 w-full rounded-xl border-3 border-border bg-bg-light p-4 flex flex-col justify-center">
                <header class="font-semibold text-3xl">
                    Mission Statement
                </header>
                <h1 class="2xl text-text-muted">
                    Aarav Kumar is a recipient of the AP Scholar with Honor award
                </h1>
            </div>

        </div>

        <div class="w-full h-full overflow-hidden rounded-xl border-3 border-border">
            <img class="object-cover w-full h-full" src="/apscholar.jpeg" alt="AP Scholar">
        </div>
    </section>

    <section class="w-[90%] mx-auto mt-[4rem]">
        <header class="font-semibold text-5xl text-center">
            Product
        </header>

        <img class="aspect-[4/1] w-full object-cover mt-16 rounded-xl border-3 border-border" src="/apscholar.jpeg" alt="AP Scholar">
    </section>

    <section class="w-full h-[10vh] text-center">
        spacer
    </section>
</main>