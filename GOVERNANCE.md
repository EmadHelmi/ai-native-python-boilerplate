# Governance

## Project Model

This project currently uses a single-maintainer governance model. Public input
and contributions are welcome, while final stewardship remains with the
repository owner.

## Roles

### Repository Owner

[`@EmadHelmi`](https://github.com/EmadHelmi) is the repository owner and final
maintainer. The owner:

- defines the reusable baseline and project scope;
- makes final decisions when consensus is not reached;
- administers releases, repository settings, and security responses;
- grants or removes collaborator and merge permissions;
- may delegate specific maintenance responsibilities.

### Authorized Collaborators

Authorized collaborators are people explicitly granted repository access by
the owner. Their permissions are limited to the access GitHub grants them and
may be changed or revoked by the owner.

Write access does not override branch protection, required checks, Code Owner
review, or the repository's approval workflow.

### Contributors

Anyone may open issues, participate constructively, fork the repository, and
submit pull requests. Contribution does not automatically grant repository
access, decision authority, or merge permission.

## Decisions

Routine contribution decisions are made through issue and pull-request review.
Meaningful changes to architecture, security, dependencies, infrastructure,
or long-term workflow follow the repository's human-controlled decision and
approval process.

The maintainer seeks relevant technical input but may accept, request changes
to, defer, or decline a proposal based on project scope and maintainability.

## Merge Authority

Only the repository owner and collaborators explicitly authorized by the owner
may merge pull requests. A pull request must also satisfy the configured
Ruleset, required status checks, review requirements, and conversation
resolution policy.

Code Owner approval is mandatory for protected branches. The owner may retain
an administrative bypass for emergency repository recovery, but ordinary
changes should follow the same pull-request process.

## Changes to Governance

Governance changes are proposed and reviewed through a pull request. They take
effect only after approval and merge by the repository owner.
