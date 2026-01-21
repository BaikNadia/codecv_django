from django.utils.html import format_html


def generate_meta_tags(profile):
    """Генерирует мета-теги для SEO"""
    return format_html(
        """
        <meta property="og:title" content="{title} - CodeCV">
        <meta property="og:description" content="{description}">
        <meta property="og:image" content="{image}">
        <meta property="og:url" content="{url}">
        <meta property="og:type" content="website">

        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="{title}">
        <meta name="twitter:description" content="{description}">

        <script type="application/ld+json">
        {{
            "@context": "https://schema.org",
            "@type": "Person",
            "name": "{name}",
            "jobTitle": "{job_title}",
            "url": "{url}",
            "sameAs": [
                "https://github.com/{github}"
            ],
            "skills": [{skills}]
        }}
        </script>
    """.format(
            title=profile.user.get_full_name() or profile.user.username,
            description=profile.bio[:160] if profile.bio else "Резюме разработчика",
            image=profile.avatar.url if profile.avatar else "",
            url=f"https://codecv.dev/cv/{profile.user.username}/",
            name=profile.user.get_full_name() or profile.user.username,
            job_title=profile.headline or "Разработчик",
            github=profile.github_username or "",
            skills=", ".join([f'"{skill.name}"' for skill in profile.skills.all()[:5]]),
        )
    )
