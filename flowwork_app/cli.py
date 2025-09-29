"""Command line interface for the Flowwork oncology application."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .care_plan import default_oncology_plan
from .reporting import build_patient_summary
from .storage import JsonStorage
from .workflow import FlowworkEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Application Flowwork pour l'oncologie")
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("data/patients.json"),
        help="Chemin du fichier de stockage JSON",
    )

    subparsers = parser.add_subparsers(dest="command")

    register = subparsers.add_parser("inscrire", help="Inscrire un nouveau patient")
    register.add_argument("identifiant")
    register.add_argument("nom_complet")
    register.add_argument("age", type=int)

    subparsers.add_parser("patients", help="Lister les patients")

    show = subparsers.add_parser("suivi", help="Afficher le suivi d'un patient")
    show.add_argument("identifiant")

    complete = subparsers.add_parser("terminer", help="Marquer une tâche comme terminée")
    complete.add_argument("identifiant")
    complete.add_argument("tache")

    return parser


def main(argv: Any = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    plan = default_oncology_plan()
    storage = JsonStorage(args.data)
    engine = FlowworkEngine(plan, storage)

    if args.command == "inscrire":
        patient = engine.register_patient(args.identifiant, args.nom_complet, args.age)
        print(json.dumps(build_patient_summary(plan, patient), indent=2, ensure_ascii=False))
        return 0

    if args.command == "patients":
        patients = [build_patient_summary(plan, p) for p in engine.list_patients()]
        print(json.dumps(patients, indent=2, ensure_ascii=False))
        return 0

    if args.command == "suivi":
        summary = engine.patient_summary(args.identifiant)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    if args.command == "terminer":
        patient = engine.complete_task(args.identifiant, args.tache)
        print(json.dumps(build_patient_summary(plan, patient), indent=2, ensure_ascii=False))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

