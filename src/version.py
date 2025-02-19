"""Version control for TodoManager."""

VERSION = "1.1.0"
VERSION_DATE = "2025-02-19"

# Version history
CHANGELOG = {
    "1.0.0": {
        "date": "2025-02-19",
        "changes": [
            "Initial release",
            "Support for hierarchical tasks",
            "Batch task import",
            "Modern UI with Light/Dark themes",
            "Pin window functionality",
            "Collapsible editing sections"
        ]
    },
    "1.1.0": {
        "date": "2025-02-19",
        "changes": [
            "Immediate task deletion without confirmation",
            "Enhanced progress visualization with color-coded progress bar",
            "Temporary success messages for task operations",
            "Comprehensive logging system",
            "Improved UI feedback for task operations",
            "Streamlined database operations",
            "Updated documentation with latest features",
            "Task deletion error handling",
            "Clear all tasks functionality",
            "Database connection issues"
        ]
    }
}

def get_version_info():
    """Get formatted version information."""
    return f"TodoManager v{VERSION} ({VERSION_DATE})"

def get_changelog():
    """Get formatted changelog."""
    changelog_text = []
    for version, info in CHANGELOG.items():
        changelog_text.append(f"\nv{version} ({info['date']})")
        for change in info['changes']:
            changelog_text.append(f"- {change}")
    return "\n".join(changelog_text)
