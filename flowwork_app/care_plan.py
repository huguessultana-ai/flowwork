"""Predefined oncology care plans."""

from __future__ import annotations

from typing import List

from .models import CarePlan, Stage, Task


def default_oncology_plan() -> CarePlan:
    """Return a default oncology care plan used by the application.

    The plan represents a typical flow for solid tumour management with
    triage, diagnostic, treatment, and survivorship stages.
    """

    stages: List[Stage] = [
        Stage(
            name="Triage initiale",
            objectives="Collecter les informations essentielles et préparer la consultation.",
            tasks=[
                Task(
                    name="Anamnèse infirmière",
                    description="Entretien infirmier pour collecter antécédents et symptômes prioritaires.",
                    due_in_days=1,
                ),
                Task(
                    name="Examens biologiques",
                    description="Programmer NFS, ionogramme, bilan hépatique et rénal.",
                    due_in_days=2,
                ),
            ],
        ),
        Stage(
            name="Diagnostic",
            objectives="Confirmer le diagnostic histologique et évaluer l'extension.",
            tasks=[
                Task(
                    name="Biopsie",
                    description="Planifier la biopsie guidée et s'assurer de l'analyse anatomopathologique.",
                    due_in_days=5,
                ),
                Task(
                    name="Imagerie",
                    description="Programmer scanner TAP ou IRM selon la localisation tumorale.",
                    due_in_days=7,
                ),
                Task(
                    name="RCP",
                    description="Présenter le dossier en réunion de concertation pluridisciplinaire.",
                    due_in_days=10,
                ),
            ],
        ),
        Stage(
            name="Traitement",
            objectives="Mettre en œuvre le traitement personnalisé validé en RCP.",
            tasks=[
                Task(
                    name="Consultation oncologue",
                    description="Informer le patient du plan thérapeutique et recueillir son consentement.",
                    due_in_days=3,
                ),
                Task(
                    name="Préparation chimiothérapie",
                    description="Coordonner la préparation pharmaceutique et la logistique d'administration.",
                    due_in_days=5,
                ),
                Task(
                    name="Suivi toxicités",
                    description="Mettre en place le suivi des effets secondaires et l'éducation thérapeutique.",
                    due_in_days=14,
                ),
            ],
        ),
        Stage(
            name="Surveillance",
            objectives="Assurer le suivi post-traitement et planifier la surveillance.",
            tasks=[
                Task(
                    name="Bilan post-thérapeutique",
                    description="Évaluer la réponse au traitement et les effets tardifs.",
                    due_in_days=30,
                ),
                Task(
                    name="Programme de surveillance",
                    description="Planifier imageries et consultations de suivi sur 12 mois.",
                    due_in_days=45,
                ),
            ],
        ),
    ]

    return CarePlan(diagnosis="Tumeur solide", stages=stages)

