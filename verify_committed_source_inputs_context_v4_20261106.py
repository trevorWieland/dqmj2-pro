import subprocess
from unittest.mock import patch
from project import ROOT, sha256
import verify_committed_source_inputs_v14_20261105 as original
from auth_context_route_v2_20261106 import validation_route
from game_overlay_reference_route_v1_20261106 import route, PROOF
from http_migration_reference_annotation_v1_20261106 import annotate


def main():
    for name in ['verify_committed_source_inputs_context_v4_20261106.py',
                 'game_overlay_reference_route_v1_20261106.py', 'http_migration_reference_annotation_v1_20261106.py']:
        assert subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT) == (ROOT / name).read_bytes()
    original_thumb = original.qualify_thumb
    annotations = []

    def qualified_thumb(batches):
        projected, notes = annotate(batches)
        annotations.extend(notes)
        return original_thumb(projected)

    write = original.write_json

    def qualified_write(path, document):
        document.update(httpMigrationNativeReferenceAnnotations=annotations, additionalMeasuredOverlayFixtureConsumer=proof,
            additionalOverlayReferenceQualificationPath=PROOF,
            additionalOverlayReferenceQualificationSha256=sha256(ROOT / PROOF),
            committedSourceInputContextWrapper='verify_committed_source_inputs_context_v4_20261106.py',
            committedSourceInputContextWrapperSha256=sha256(ROOT / 'verify_committed_source_inputs_context_v4_20261106.py'),
            originalOverlayQualifierRegistryIdentityAndAllOtherConsumerGuardsRetained=True)
        write(path, document)

    with validation_route(), route() as proof, patch.object(original, 'write_json', qualified_write), patch.object(original, 'qualify_thumb', qualified_thumb):
        original.main()


if __name__ == '__main__':
    main()
