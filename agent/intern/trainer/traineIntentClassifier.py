import random
import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path
from dataTraine import EXEMPLOS_TREINO, INTENT_LABELS


def main():
    nlp = spacy.blank("pt")

    if "textcat" not in nlp.pipe_names:
        textcat = nlp.add_pipe("textcat", last=True)
    else:
        textcat = nlp.get_pipe("textcat")

    for label in INTENT_LABELS:
        textcat.add_label(label)

    TRAIN_DATA = []
    for texto, rotulo in EXEMPLOS_TREINO:
        TRAIN_DATA.append(
            (texto, {"cats": {rot: (rot == rotulo) for rot in INTENT_LABELS}}))

    n_iter = 50
    optimizer = nlp.begin_training()

    with nlp.select_pipes(enable="textcat"):
        nlp.begin_training()
        for epoch in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            batches = minibatch(TRAIN_DATA, size=compounding(2.0, 16.0, 1.2))
            for batch in batches:
                examples = [Example.from_dict(
                    nlp.make_doc(text), ann) for text, ann in batch]
                nlp.update(examples, drop=0.3, losses=losses, sgd=optimizer)
            print(f"Epoch {epoch+1}/{n_iter} - Loss: {losses['textcat']:.3f}")

    output_dir = Path("model_classifier")
    output_dir.mkdir(parents=True, exist_ok=True)
    nlp.to_disk(output_dir)
    print(f"Modelo salvo em: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
