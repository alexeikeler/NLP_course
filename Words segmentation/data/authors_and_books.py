from typing import List


class TextData:

    def __init__(self):

        self.__authors_data = {
            'Friedrich Nietzsche': [
                'Beyond good and evil',
                'Thus Spake Zarathustra: A Book for All and None',
                'The Antichrist'
            ],

            'Franz Kafka': [
                'The Trial',
                'Metamorphosis'
            ],

            'Arthur Schopenhauer': [
                'The World as Will and Idea (Vol. 1 of 3)',
                'Essays of Schopenhauer',
                'The Basis of morality'
            ]
        }

        self.__sentences = {

        ('Friedrich Nietzsche', 'Beyond good and evil'):

            ['How malicious philosophers can be',

             'Philosophers are accustomed to speak of the will as though it were '
             'the best known thing in the world indeed, Schopenhauer has given us '
             'to understand that the will alone is really known to us absolutely and '
             'completely known without deduction or addition',

             'A new order of philosophers is appearing I shall venture to baptize '
             'them by a name not without danger'],

        ('Friedrich Nietzsche', 'Thus Spake Zarathustra: A Book for All and None'):

            ['Away from God and Gods did this will allure me what would there be to '
             'create if there were Gods',

             'And they knew not how to love their God otherwise '
             'than by nailing men to the cross',

             'My friends I will not be mixed up and confounded with others'],

        ('Friedrich Nietzsche', 'The Antichrist'):

            ['Among Germans I am immediately understood when '
             'I say that theological blood is the ruin of philosophy',

             'Buddhism I repeat is a hundred times more austere '
             'more honest more objective.',
             
             'I have already given my answer to the problem'],

        ('Franz Kafka', 'Metamorphosis'):
            ['One morning when Gregor Samsa woke from troubled dreams '
             'he found himself transformed in his bed into a horrible vermin',

             'Because he had to open the door in this way '
             'it was already wide open before he could be seen',

             'After that the three of them left the flat together '
             'which was something they had not done for months '
             'and took the tram out to the open country outside the town'],

        ('Franz Kafka', 'The Trial'):
            ['It was already gone half past eleven when '
             'someone could be heard in the stairway',

             'The weather was dull on Sunday',

             'Without having intended it he had raised his voice'],

        ('Arthur Schopenhauer', 'The World as Will and Idea (Vol. 1 of 3)'):
            ['But time and space each for itself can be mentally presented apart from '
             'matter whereas matter cannot be so presented apart from time and space',

             'After these numerous quotations from the poets perhaps '
             'I also may be allowed to express myself by a metaphor',

             'For the present however in this first book we '
             'consider everything merely as idea as object for the subject'],

        ('Arthur Schopenhauer', 'Essays of Schopenhauer'):
            ['When Schopenhauer was asked where he wished to be buried, he answered '
             '\" Anywhere they will find me \" and the stone that marks his grave at '
             'Frankfort bears merely the inscription Arthur Schopenhauer without '
             'even the date of his birth or death',

             'These essays are a valuable criticism of life by a man who had a wide '
             'experience of life, a man of the world, who possessed an almost inspired '
             'faculty of observation',

             'There are first of all two kinds of authors those who write for the '
             'subject\'s sake, and those who write for writing\'s sake'],

        ('Arthur Schopenhauer', 'The Basis of morality'):
            ['In giving way to emotion of this violent kind the greatest genius '
             'puts himself on a level with the commonest son of earth',

             'And even in the drama which is the peculiar province of the passions '
             'and emotions it is easy for them to appear common and vulgar',

             'Why is it that in spite of all the mirrors in the world no one '
             'really knows what he looks like?'],

    }

    def get_authors(self) -> List[str]:
        return [author for author, _ in self.__authors_data.items()]

    def get_books(self, author: str) -> List[str]:
        return self.__authors_data[author]

    def get_sentences(self, author: str, book: str) -> List[str]:
        return self.__sentences[author, book]
