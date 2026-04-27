"""
seed.py — Run this once to populate the database with sample content.

  python seed.py
"""

from datetime import datetime, timezone

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from adapters.orm_models import Article, Author, Category, Tag
from config import DATABASE_URL

ENGINE = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, expire_on_commit=False)
SESSION = SessionLocal()

# ── Authors ───────────────────────────────────────────────────────────────────
authors = [
    {
        "name": "Dr. Evelyn Marsh",
        "bio": "Clinical psychologist and Jungian analyst with 15 years of practice. Author of *The Hidden Self*.",
        "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100&q=80",
    },
    {
        "name": "Rohan Voss",
        "bio": "Neuroscientist and science communicator. PhD from MIT, writes about consciousness and the brain.",
        "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&q=80",
    },
    {
        "name": "Anika Selin",
        "bio": "Mindfulness researcher and certified MBSR instructor. Explores the intersection of ancient wisdom and modern psychology.",
        "avatar_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80",
    },
]

for row in authors:
    exists = SESSION.execute(select(Author).where(Author.name == row["name"])).scalar_one_or_none()
    if not exists:
        SESSION.add(Author(**row))

# ── Categories ────────────────────────────────────────────────────────────────
categories = [
    {
        "name": "Mental Health",
        "slug": "mental-health",
        "description": "Exploring emotional wellbeing, therapy, and the journey toward psychological resilience.",
    },
    {
        "name": "Neuroscience",
        "slug": "neuroscience",
        "description": "Diving deep into the brain's architecture — how we think, feel, and perceive reality.",
    },
    {
        "name": "Mindfulness",
        "slug": "mindfulness",
        "description": "Ancient practices, modern evidence — cultivating presence and inner peace.",
    },
    {
        "name": "Therapy",
        "slug": "therapy",
        "description": "Therapeutic modalities, case studies, and the science of healing.",
    },
    {
        "name": "Well-being",
        "slug": "well-being",
        "description": "Holistic approaches to living a flourishing, meaningful life.",
    },
    {
        "name": "Consciousness",
        "slug": "consciousness",
        "description": "The great mystery — exploring awareness, dreams, and altered states.",
    },
]

for row in categories:
    exists = SESSION.execute(select(Category).where(Category.slug == row["slug"])).scalar_one_or_none()
    if not exists:
        SESSION.add(Category(**row))

# ── Tags ──────────────────────────────────────────────────────────────────────
tags = [
    ("Jung", "jung"),
    ("Shadow Work", "shadow-work"),
    ("CBT", "cbt"),
    ("Trauma", "trauma"),
    ("Dreams", "dreams"),
    ("Meditation", "meditation"),
    ("Neuroplasticity", "neuroplasticity"),
    ("Anxiety", "anxiety"),
    ("Depression", "depression"),
    ("Healing", "healing"),
    ("Resilience", "resilience"),
    ("Psychotherapy", "psychotherapy"),
    ("Consciousness", "consciousness"),
    ("Sleep", "sleep"),
    ("Identity", "identity"),
]

for name, slug in tags:
    exists = SESSION.execute(select(Tag).where(Tag.slug == slug)).scalar_one_or_none()
    if not exists:
        SESSION.add(Tag(name=name, slug=slug))

SESSION.commit()

# ── Articles ──────────────────────────────────────────────────────────────────
articles = [
    {
        "title": "Understanding the Shadow Self — A Guide to Jungian Psychology",
        "slug": "understanding-the-shadow-self-jungian-psychology",
        "excerpt": "Dive deep into the unconscious and embrace the parts of yourself you have hidden away. Carl Jung's concept of the Shadow is one of the most transformative ideas in psychology.",
        "content": """
## What Is the Shadow Self?

Carl Gustav Jung introduced the concept of the **Shadow** to describe the unconscious part of the psyche that contains repressed ideas, weaknesses, desires, instincts, and shortcomings. It is the "dark side" of our personality — not in the sense of evil, but in the sense of what is hidden from our conscious awareness.

> "One does not become enlightened by imagining figures of light, but by making the darkness conscious." — Carl Jung

## Why Do We Have a Shadow?

From childhood, we learn which parts of ourselves are acceptable and which are not. A child who is told that anger is bad will suppress anger, pushing it into the shadow. Over time, this creates a **persona** — the mask we wear — and a shadow that grows in proportion.

## Integrating the Shadow

Shadow work is the process of bringing these hidden aspects into conscious awareness. This doesn't mean acting on every dark impulse — it means *understanding* them with compassion.

**Practical steps to begin shadow work:**

1. **Journaling** — Write about reactions that feel disproportionately strong
2. **Dream Analysis** — Pay attention to recurring figures in dreams
3. **Notice projections** — The qualities that irritate you most in others often mirror your own shadow
4. **Seek a therapist** — A Jungian analyst can guide deep shadow integration safely

## The Gifts of the Shadow

Integration doesn't just remove darkness — it *reveals* gifts. Suppressed creativity, passion, and authentic self-expression often live in the shadow, waiting to be reclaimed.

The shadow self, when integrated, becomes a source of enormous psychological energy and genuine self-knowledge.
""",
        "cover_image_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1200&q=80",
        "category": "mental-health",
        "author": "Dr. Evelyn Marsh",
        "is_featured": True,
        "reading_time": 8,
        "tags": ["jung", "shadow-work", "identity"],
    },
    {
        "title": "The Architecture of Anxiety — What Your Brain Is Actually Doing",
        "slug": "architecture-of-anxiety-what-your-brain-is-doing",
        "excerpt": "Anxiety isn't a character flaw. It's a feature of an ancient threat-detection system running in a modern world. Here's the neuroscience.",
        "content": """
## The Anxious Brain

Anxiety is one of the most common human experiences, yet it remains deeply misunderstood. At its core, anxiety is a **survival mechanism** — a neural alarm system that evolved over millions of years to keep us alive.

## The Amygdala: Your Inner Smoke Detector

The amygdala is a small, almond-shaped structure deep in the brain that acts as the primary threat-detection centre. When it perceives danger — real or imagined — it triggers a cascade of physiological responses we know as the **fight-or-flight response**.

The problem? The amygdala cannot distinguish between a tiger and a difficult conversation. To it, both are potential threats.

## The Prefrontal Cortex: The Rational Voice

The prefrontal cortex (PFC) is the seat of rational thought. In healthy anxiety regulation, the PFC communicates with the amygdala, essentially saying: *"Relax, it's not actually a tiger."*

In anxiety disorders, this communication is disrupted. The amygdala runs hot, and the PFC struggles to regulate it.

## Neuroplasticity and Hope

Here's the genuinely exciting part: the brain can change. Practices like **cognitive-behavioural therapy (CBT)**, **mindfulness meditation**, and even regular aerobic exercise have been shown to literally reshape the neural circuits underlying anxiety.

This is neuroplasticity in action — your brain rewiring itself toward greater calm and regulation.
""",
        "cover_image_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=1200&q=80",
        "category": "neuroscience",
        "author": "Rohan Voss",
        "is_featured": True,
        "reading_time": 7,
        "tags": ["anxiety", "neuroplasticity", "cbt"],
    },
    {
        "title": "The Psychology of Dreams — Windows to the Unconscious",
        "slug": "psychology-of-dreams-windows-to-the-unconscious",
        "excerpt": "Every night you enter a strange theatre where time collapses, the impossible happens, and your deepest fears and desires take form. What are dreams, really?",
        "content": """
## The Dream Theatre

For as long as humans have existed, we have been dreaming. Ancient Egyptians believed dreams were messages from the gods. Freud called them *the royal road to the unconscious*. Modern neuroscience sees them as a byproduct of memory consolidation.

The truth, as is often the case, is more nuanced and more beautiful than any single theory.

## Freudian Dream Theory

Sigmund Freud proposed that dreams represent **wish fulfilment** — disguised expressions of repressed desires, primarily sexual and aggressive impulses that the conscious mind finds unacceptable.

While modern psychologists view Freud's specific mechanisms with scepticism, his fundamental insight — that dreams connect to our emotional and psychological lives — has proven remarkably durable.

## Jungian Dream Analysis

Jung diverged from Freud by seeing dreams not as disguised wishes but as **honest communications from the unconscious**. For Jung, dream symbols were not personally coded but drew from a shared reservoir of human imagery — the **collective unconscious**.

## The Neuroscience of Dreaming

Modern sleep science has mapped dreaming primarily to **REM (Rapid Eye Movement) sleep**. During REM, the limbic system (emotional centres) is highly active while the prefrontal cortex is relatively quiet — which may explain why dreams are emotionally vivid yet narratively bizarre.

The **memory consolidation hypothesis** suggests that dreaming helps the brain process and integrate experiences from waking life.

## Working With Your Dreams

Keep a dream journal by your bed. Write immediately upon waking. Over time, patterns emerge — recurring symbols, settings, characters — that can illuminate your psychological landscape with remarkable precision.
""",
        "cover_image_url": "https://images.unsplash.com/photo-1451188502541-13943edb6acb?w=1200&q=80",
        "category": "consciousness",
        "author": "Dr. Evelyn Marsh",
        "is_featured": True,
        "reading_time": 9,
        "tags": ["dreams", "jung", "consciousness"],
    },
    {
        "title": "Resilience: Building Inner Strength Through Adversity",
        "slug": "resilience-building-inner-strength",
        "excerpt": "Resilience is not about never falling. It is about learning to rise — and the science reveals that this capacity can be deliberately cultivated.",
        "content": """
## What Is Resilience?

Resilience is the psychological capacity to adapt to stress, adversity, trauma, and tragedy. It is not the absence of distress but the ability to navigate through it and emerge with one's sense of self intact — often stronger.

## The Three Pillars of Resilience

Research across psychology and neuroscience has identified several core factors:

### 1. Social Connection
Humans are profoundly social animals. Strong relationships — feeling seen, heard, and supported — are the most robust predictor of resilience across cultures.

### 2. Meaning-Making
Viktor Frankl, who survived Nazi concentration camps and wrote *Man's Search for Meaning*, observed that those who found meaning in their suffering were more likely to survive psychologically. The capacity to construct a coherent narrative around adversity is central to resilience.

### 3. Regulatory Skills
The ability to tolerate and regulate difficult emotions — to feel fear without being consumed by it — is a learnable skill, one that sits at the heart of therapies like DBT and mindfulness-based interventions.

## Building Your Resilience Capacity

- **Practice self-compassion** — Treat yourself as you would a dear friend
- **Develop a growth mindset** — Adversity as teacher, not punishment
- **Invest in relationships** — Vulnerability builds connection
- **Seek professional support** — There is strength in asking for help
""",
        "cover_image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=1200&q=80",
        "category": "well-being",
        "author": "Anika Selin",
        "is_featured": False,
        "reading_time": 6,
        "tags": ["resilience", "healing", "trauma"],
    },
    {
        "title": "Trauma & Recovery — The Body Keeps the Score",
        "slug": "trauma-recovery-body-keeps-the-score",
        "excerpt": "Trauma is not just a memory. It lives in the body, in the nervous system, in the way we breathe and hold ourselves. Understanding this changes everything about healing.",
        "content": """
## Trauma Is Physiological

Bessel van der Kolk's landmark work established something radical for its time: trauma is not just a psychological phenomenon — it is a physiological one. The body literally holds traumatic experiences in the nervous system, in muscle tension, in breath patterns, in our very biology.

## The Window of Tolerance

The **Window of Tolerance** is a therapeutic concept describing the optimal zone of nervous system activation within which we can function effectively. Trauma narrows this window, leaving people oscillating between hyperarousal (panic, rage) and hypoarousal (shutdown, dissociation).

Recovery involves gradually widening this window through safe, titrated exposure and somatic (body-based) practices.

## Somatic Approaches to Healing

Body-based therapies have emerged as powerful complements to traditional talk therapy:

- **Somatic Experiencing (SE)** — developed by Peter Levine
- **EMDR** — Eye Movement Desensitisation and Reprocessing
- **Sensorimotor Psychotherapy**
- **Yoga and movement therapies**

These approaches work *with* the body, not just the mind, to process and release stored traumatic responses.

## The Healing Arc

Recovery from trauma is not linear. It spirals — revisiting material at greater depth as the capacity to tolerate it grows. With appropriate support, the possibility of genuine post-traumatic *growth* is real and documented.
""",
        "cover_image_url": "https://images.unsplash.com/photo-1542822038-297a1a66a5bc?w=1200&q=80",
        "category": "therapy",
        "author": "Dr. Evelyn Marsh",
        "is_featured": False,
        "reading_time": 10,
        "tags": ["trauma", "healing", "psychotherapy"],
    },
    {
        "title": "The Science of Meditation — What Happens When You Sit in Silence",
        "slug": "science-of-meditation-what-happens-when-you-sit",
        "excerpt": "Thousands of years of contemplative wisdom now under the MRI scanner. What does modern neuroscience actually reveal about the meditating brain?",
        "content": """
## Meditation Enters the Lab

Once dismissed as mysticism, meditation is now one of the most rigorously studied psychological interventions. The last three decades have produced thousands of peer-reviewed studies examining its effects on brain structure, function, and mental health.

## What Changes in the Brain

Long-term meditators show measurable differences in brain structure:

- **Thicker prefrontal cortex** — associated with attention and self-regulation
- **Reduced amygdala reactivity** — the brain's alarm centre becomes quieter
- **Increased grey matter** in regions associated with learning and emotional regulation
- **Enhanced default mode network regulation** — less mind-wandering

## The Different Flavours of Meditation

Not all meditation is the same, and the neuroscience reflects this:

- **Focused Attention (FA)** — concentrating on a single object (breath, mantra). Trains attentional control.
- **Open Monitoring (OM)** — open awareness of all arising phenomena. Develops metacognitive capacity.
- **Loving-Kindness (Metta)** — generating warm feelings toward self and others. Activates prosocial neural circuits.

## Starting a Practice

The research consistently shows that even **8 weeks of regular practice** produces measurable changes in brain and wellbeing. You don't need a retreat or decades of practice.

Start with 10 minutes a day. The breath is always available.
""",
        "cover_image_url": "https://images.unsplash.com/photo-1447452001602-7090c7ab2db3?w=1200&q=80",
        "category": "mindfulness",
        "author": "Anika Selin",
        "is_featured": False,
        "reading_time": 7,
        "tags": ["meditation", "neuroplasticity", "consciousness"],
    },
    {
        "title": "Cognitive Distortions — The Lies Your Mind Tells You",
        "slug": "cognitive-distortions-lies-your-mind-tells-you",
        "excerpt": "All-or-nothing thinking, catastrophising, mind reading — our brains run habitual distortions that warp reality and fuel suffering. Learn to recognise and challenge them.",
        "content": """
## The Distorting Brain

Aaron Beck, the father of cognitive therapy, made a revolutionary observation: depression and anxiety are maintained not by circumstances but by *patterns of thinking* — systematic errors in reasoning he called **cognitive distortions**.

## The Major Distortions

**All-or-nothing thinking:** Seeing in black and white, with no shades of grey. "I made one mistake, therefore I'm a total failure."

**Catastrophising:** Automatically assuming the worst-case scenario. "I'm nervous about this presentation — I'll definitely humiliate myself."

**Mind reading:** Assuming you know what others are thinking. "They haven't replied — they must be angry with me."

**Emotional reasoning:** "I feel worthless, therefore I *am* worthless."

**Should statements:** Rigid rules about how you and others *must* behave, generating guilt and resentment.

**Personalisation:** Taking excessive responsibility for events outside your control.

## Challenging Distortions: The CBT Method

1. **Identify** the distortion
2. **Question the evidence** — What supports this thought? What contradicts it?
3. **Generate alternatives** — What's another way to interpret this situation?
4. **Examine the consequences** — Is this thought helpful or harmful?
5. **Reframe** — Construct a more balanced, realistic perspective

With practice, this becomes automatic — literally rewiring the default narrative of the mind.
""",
        "cover_image_url": "https://images.unsplash.com/photo-1580894732444-8ecded7900cd?w=1200&q=80",
        "category": "mental-health",
        "author": "Dr. Evelyn Marsh",
        "is_featured": False,
        "reading_time": 6,
        "tags": ["cbt", "anxiety", "depression"],
    },
    {
        "title": "Neuroplasticity — Your Brain Is Not Fixed",
        "slug": "neuroplasticity-your-brain-is-not-fixed",
        "excerpt": "For most of history, scientists believed the adult brain was essentially fixed. We now know this is profoundly wrong — and the implications for human potential are extraordinary.",
        "content": """
## The Old Paradigm

For much of the 20th century, mainstream neuroscience held that the adult brain was essentially static — neurons were what they were, and what was lost could not be regained. This view has been overturned by one of the most significant scientific discoveries of recent decades.

## What Is Neuroplasticity?

Neuroplasticity refers to the brain's lifelong ability to reorganise itself by forming new neural connections. It encompasses:

- **Synaptic plasticity** — strengthening or weakening of existing connections
- **Neurogenesis** — the birth of new neurons (primarily in the hippocampus)
- **Cortical remapping** — large-scale reorganisation of brain regions

## Hebb's Law: The Fundamental Principle

Donald Hebb formulated the foundational principle of neuroplasticity: *"Neurons that fire together, wire together."*

Every time you have a thought, practise a skill, or experience an emotion, neural pathways are activated. Repeated activation strengthens these pathways — making certain thoughts, emotions, and behaviours more automatic.

## Practical Implications

This is deeply hopeful: the patterns that cause suffering — anxious rumination, depressive thinking, addictive loops — are learned. And what is learned can be unlearned.

Deliberate practice, therapy, meditation, exercise, and even sleep are all forms of intentional neuroplastic change.

The brain you have today is not the brain you must have tomorrow.
""",
        "cover_image_url": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=1200&q=80",
        "category": "neuroscience",
        "author": "Rohan Voss",
        "is_featured": False,
        "reading_time": 8,
        "tags": ["neuroplasticity", "healing"],
    },
    {
        "title": "The Silence Between Thoughts — An Introduction to Mindfulness",
        "slug": "silence-between-thoughts-introduction-to-mindfulness",
        "excerpt": "Mindfulness is not about emptying the mind. It is about changing your relationship to what arises in it — and that changes everything.",
        "content": """
## A Common Misconception

Most people believe that meditation means having no thoughts. When thoughts inevitably arise during practice, they conclude: "I'm bad at this." This misunderstanding is perhaps the biggest obstacle to developing a meditation practice.

Mindfulness is not the absence of thought. It is **non-reactive awareness** of thought — the capacity to observe mental events as they arise and pass, without being hijacked by them.

## The Core Skill: Stepping Back

The foundational movement of mindfulness is a kind of internal stepping back — from *being* a thought to *observing* a thought. Psychologists call this **metacognitive awareness** or **decentring**.

When you are lost in anxious thoughts, you *are* the anxiety. When you observe "there's anxiety arising in me right now," you have stepped back into a more spacious relationship with experience.

## The Formal Practice

Mindfulness-Based Stress Reduction (MBSR), developed by Jon Kabat-Zinn at the University of Massachusetts, is the most well-researched mindfulness programme. An 8-week course with robust evidence for:

- Reduced anxiety and depression symptoms
- Improved immune function
- Better sleep quality
- Enhanced pain tolerance

## Informal Practice

The most powerful aspect of mindfulness is that it can be practised anywhere, anytime. Washing dishes, walking, listening to a friend — any activity can become an opportunity for presence.

The practice is always the same: notice that attention has wandered, and gently return.
""",
        "cover_image_url": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=1200&q=80",
        "category": "mindfulness",
        "author": "Anika Selin",
        "is_featured": False,
        "reading_time": 5,
        "tags": ["meditation", "anxiety", "healing"],
    },
]

for art in articles:
    category = SESSION.execute(
        select(Category).where(Category.slug == art["category"])
    ).scalar_one_or_none()
    if not category:
        continue

    author = SESSION.execute(
        select(Author).where(Author.name == art["author"])
    ).scalar_one_or_none()

    existing = SESSION.execute(
        select(Article).where(Article.slug == art["slug"])
    ).scalar_one_or_none()
    if existing:
        continue

    article = Article(
        title=art["title"],
        slug=art["slug"],
        excerpt=art["excerpt"],
        content=art["content"],
        cover_image_url=art["cover_image_url"],
        category_id=category.id,
        author_id=author.id if author else None,
        is_featured=art["is_featured"],
        reading_time_minutes=art["reading_time"],
        published_at=datetime.now(timezone.utc),
    )

    for tag_slug in art.get("tags", []):
        tag = SESSION.execute(select(Tag).where(Tag.slug == tag_slug)).scalar_one_or_none()
        if tag:
            article.tags.append(tag)

    SESSION.add(article)

print("✅  Seed data inserted successfully.")
SESSION.commit()
SESSION.close()
