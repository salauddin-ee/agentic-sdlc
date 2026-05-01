# Existing system analysis — TrainAssist

> **Status:** Draft
> **Version:** 0.1.0

## Tech stack
| Component | Technology | Version | Notes |
|---|---|---|---|
| Language | JavaScript/React | - | SPA built with Vite |
| Runtime | Browser | - | |
| Framework | React (likely) | - | Uses `root` div and index.js bundle |
| API Base | `/api` | - | Endpoints identified: `/api/auth/sso/google/login`, `/api/companies/` |
| Auth | Bearer Token | - | Stored in LocalStorage |

## Test coverage baseline
- Total tests: [N/A]
- Passing: [N/A]
- Failing: [N/A]
- Coverage: [N/A]
- Last run: [N/A]

**Note: No source code access; analysis performed via browser content and JS bundle exploration.**

## Existing patterns
- Error handling: Returns JSON with `error` or `detail` keys.
- Logging: Task submissions log prompts and responses with `|||PROMPT|||` and `|||RESPONSE|||` tags.
- Input validation: Client-side validation exists for emails and names; server-side validation suspected.
- Directory structure: Assets in `/assets/`.

## Known tech debt
- [N/A]

## Integration points
| Integration | Direction | Protocol | Notes |
|---|---|---|---|
| Google SSO | outbound | OAuth2 | Used for authentication |
| Claude Code | inbound/outbound | - | Terminal interface for training |

## Fragile / high-risk areas
- **Bulk Invite Endpoint**: `/api/companies/${a}/members/bulk-invite` - Risk of DoS or injection.
- **Task Submission**: `/api/tasks/${taskId}/submit` - Risk of sandbox escape if the terminal is not isolated.
- **Role Management**: Risks of privilege escalation if roles like `super_admin` can be set by unauthorized users.

## Constraints
- No direct backend access.
- Limited to public endpoints and client-side code analysis.
