import pandas as pd
import os

# Create a sample dataset with BOTH REAL and FAKE news
sample_data = {
    'title': [
        # REAL examples
        'Scientists Discover New Species of Deep-Sea Fish',
        'Global Stock Markets Rise On Positive Economic Data',
        'Environmental Groups Celebrate New Conservation Policy',
        'Tech Company Launches New Battery Technology',
        'University Researchers Publish Peer-Reviewed Study',
        # FAKE examples
        'Secret Government Program Controls Weather Using Technology',
        'Celebrity Announces Shocking Secret That Will Change Everything',
        'Miracle Cure Discovered That Doctors Don\'t Want You To Know',
        'Politician Caught In Unverified Scandal',
        'Mysterious Object Spotted In Sky Raises UFO Questions'
    ],
    'text': [
        # REAL examples
        'Researchers from the Marine Biology Institute announced today the discovery of a previously unknown species of bioluminescent fish at a depth of 2000 meters. The discovery was made during a collaborative expedition sponsored by the National Science Foundation.',
        'Major stock indices around the world rallied today following the release of better-than-expected quarterly earnings reports from leading technology companies. The S&P 500 index rose 2.3% in today\'s trading session.',
        'The World Wildlife Fund and other environmental organizations praised today\'s announcement of new protections for endangered species habitat. The policy was developed in consultation with scientific experts and indigenous communities.',
        'A leading technology company unveiled a new solid-state battery technology that promises to double the energy density of current lithium-ion batteries. The breakthrough was achieved after five years of research and development.',
        'Researchers at a major university published findings in a peer-reviewed journal showing positive results from a new medical treatment. The study involved 500 participants over a two-year period.',
        # FAKE examples
        'Anonymous sources claim the government has been secretly controlling weather using advanced technology hidden from the public. The program allegedly costs billions of dollars and is controlled by an elite group.',
        'In an exclusive interview, a famous celebrity revealed information that will supposedly shake the foundations of modern society. The celebrity refused to provide specific details but promised more revelations soon.',
        'A natural health blogger claims to have found a simple cure for a common disease that major pharmaceutical companies are allegedly suppressing. No scientific evidence or studies are provided to support the claims.',
        'According to unnamed sources, a politician allegedly engaged in unethical behavior. The claims have not been verified by any credible news sources and lack supporting documentation.',
        'Residents report seeing unusual lights in the sky with no explanation. While officials suggest it was likely a weather balloon or satellite, a UFO enthusiast claims it proves alien visitation.'
    ],
    'label': [
        # REAL
        'REAL', 'REAL', 'REAL', 'REAL', 'REAL',
        # FAKE
        'FAKE', 'FAKE', 'FAKE', 'FAKE', 'FAKE'
    ]
}

# Create DataFrame
df = pd.DataFrame(sample_data)

# Save to CSV
df.to_csv('news_from_openai.csv', index=False)

print("\n" + "="*60)
print("✅ Sample Dataset Created")
print("="*60)
print(f"\n✓ Created: news_from_openai.csv")
print(f"✓ Total articles: {len(df)}")
print(f"\nLabel distribution:")
print(df['label'].value_counts())
print("\nNext step: python train_model_enhanced.py\n")
