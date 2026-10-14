"""Locked copy reused by more than one generator. No em dashes."""

# rows from section 6 of Trisian_Website_Architecture.html. A dash in the source renders as "Not included".
Y = '✓'
NO = 'none'
CMP = [
    ('Workspace and infrastructure', [
        ('Microsoft 365 License', 'Business Premium', 'E3', 'E5'),
        ('CIS-Hardened Images', NO, Y, Y),
        ('Customized Industry Images', NO, NO, Y),
        ('Multi-Region Infrastructure', NO, NO, Y)]),
    ('Security', [
        ('Endpoint Protection', 'Standard AV', 'Behavioral (P1)', 'Full EDR + Hunting (P2)'),
        ('Email Security', 'Anti-spam', 'Advanced anti-phishing', 'Attack simulation'),
        ('Identity Protection', 'MFA + CA', 'Risk-based sign-in', 'PIM + P2'),
        ('Data Loss Prevention', 'Basic', 'Enhanced', 'Advanced + auto-label'),
        ('SIEM/SOAR + Zero Trust', NO, NO, Y)]),
    ('Monitoring', [
        ('24×7 Platform Monitoring', Y, Y, Y),
        ('User Experience Monitoring', NO, Y, Y)]),
    ('Compliance', [
        ('Audit Log Retention', '180 days', '180 days', '1 year'),
        ('eDiscovery', 'Standard', 'Standard', 'Premium'),
        ('Automated Compliance Suite', NO, NO, Y)]),
    ('Support and SLA', [
        ('Support Window', 'Business Hours', '24/7/365', '24/7/365'),
        ('P1 Critical Response', '1 hour', '1 hour', '30 minutes'),
        ('P2 High Response', '4 hours', '4 hours', '2 hours'),
        ('Dedicated Team + TAM', NO, NO, Y)]),
]




FAQ = [
    ('What exactly is Safe Workspace?',
     "A cloud desktop environment built on Azure Virtual Desktop or Citrix Cloud. It bundles Microsoft 365, endpoint security, monitoring, compliance and support into one platform, run entirely by Trisian. Your team logs in. We handle everything underneath."),
    ('If desktops wipe every night, what happens to our files?',
     "They stay. Profiles and files live in separate, managed storage, so people sign in to a fresh desktop with their work exactly where they left it. Only the machine resets."),
    ('Which regulations do you cover?',
     "HIPAA, SOC 2, PCI-DSS, GDPR, SOX, DORA, CMMC, GLBA and ISO 27001. The assessment maps them to your business, so you see which ones actually apply to you."),
    ('How does pricing work?',
     "Three lines. A per-user monthly platform fee that covers everything automated, including Microsoft 365 licensing. Contracted support hours for the human work, every hour logged. And projects, scoped and quoted separately. Azure is billed at cost, with no markup."),
    ('Do you replace our IT team?',
     "No. Trisian works co-managed and augments the people you already have. Your team keeps the context. We take the load and the 2am calls."),
    ('How do we know which plan fits?',
     "The assessment decides. We score your security, performance and compliance against your user count, your industry and your regulators, then recommend a plan and show our reasoning."),
    ('What happens outside business hours?',
     "Advanced and Enterprise include 24/7/365 support at the same rate. Every plan has emergency escalation through your named contacts."),
    ('How long does it take to go live?',
     "A typical rollout runs 90 days. Days 1 to 30: platform and pilot group. Days 31 to 60: full migration and training. Days 61 to 90: optimization, compliance validation and steady state. Bigger environments take longer."),
    ('Can you move us off Citrix or VMware?',
     "Yes. We migrate from Citrix and VMware Horizon to Azure Virtual Desktop, keeping profiles and settings. Migrations are scoped and quoted as projects."),
    ('What happens in an assessment?',
     "We review your current environment against the rules you answer to, then tell you where the day-after meeting would go badly today and which plan closes the gap."),
    ('What does Azure actually cost us?',
     "What Azure charges. It's billed as a straight pass-through with full visibility, and Trisian adds no markup. We optimize the spend and profit nothing on it."),
]


