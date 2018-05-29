import graphene
from graphene import Node, relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.models import Account, Cashier, Clasification, Transaction
from django.contrib.auth.models import User


class UserNode(DjangoObjectType):
    """
    Users
    """
    class Meta:
        model = User
        filter_fields = ['username', 'first_name', 'last_name', 'email', ]
        interfaces = (Node, )


class AccountNode(DjangoObjectType):
    """
    Accounts
    """
    class Meta:
        model = Account
        filter_fields = ['user', 'name', ]
        interfaces = (Node, )


class CashierNode(DjangoObjectType):
    """
    Cashiers
    """
    class Meta:
        model = Cashier
        filter_fields = ['account', 'name', ]
        interfaces = (Node, )


class ClasificationNode(DjangoObjectType):
    """
    Clasifications
    """
    class Meta:
        model = Clasification
        filter_fields = ['account', 'name', ]
        interfaces = (Node, )


class TransactionNode(DjangoObjectType):
    """
    Transactions
    """
    class Meta:
        model = Transaction
        filter_fields = ['user', 'payment', 'description', 'date', 'clasification', 'account', ]
        interfaces = (Node, )


class Query(object):
    user = Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    account = Node.Field(AccountNode)
    all_accounts = DjangoFilterConnectionField(AccountNode)

    cashier = Node.Field(CashierNode)
    all_cashiers = DjangoFilterConnectionField(CashierNode)

    clasification = Node.Field(ClasificationNode)
    all_clasifications = DjangoFilterConnectionField(ClasificationNode)

    transaction = Node.Field(TransactionNode)
    all_transactions = DjangoFilterConnectionField(TransactionNode)


class CreateAccountMutation(relay.ClientIDMutation):
    class Input:
        user_id = graphene.ID(required=True)
        name = graphene.String(required=True)

    account = graphene.Field(AccountNode)
    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, user_id, name, client_mutation_id=None):
        user = Node.get_node_from_global_id(info, user_id)
        name = name

        account = Account.objects.filter(user=user, name=name).first()

        assert account is None, 'Account exists: {0}'.format(
            Node.to_global_id('AccountNode', account.id)
        )

        account = Account.objects.create(user=user, name=name)
        success = True

        return CreateAccountMutation(account=account, success=success)


class DeleteAccountMutation(relay.ClientIDMutation):
    class Input:
        account_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, account_id):
        account = Node.get_node_from_global_id(info, account_id)

        assert account is not None, 'Account not exists'

        account.delete()
        return DeleteAccountMutation(success=bool(account))


class CreateCashierMutation(relay.ClientIDMutation):
    class Input:
        account_id = graphene.ID(required=True)
        name = graphene.String(required=True)

    cashier = graphene.Field(CashierNode)
    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, account_id, name, client_mutation_id=None):
        account = Node.get_node_from_global_id(info, account_id)
        name = name

        cashier = Cashier.objects.filter(account=account, name=name).first()

        assert cashier is None, 'Cashier exists: {0}'.format(
            Node.to_global_id('CashierNode', cashier.id)
        )

        cashier = Cashier.objects.create(account=account, name=name)
        success = True

        return CreateCashierMutation(cashier=cashier, success=success)


class DeleteCashierMutation(relay.ClientIDMutation):
    class Input:
        cashier_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, cashier_id):
        cashier = Node.get_node_from_global_id(info, cashier_id)

        assert cashier is not None, 'Cashier not Exists'

        cashier.delete()
        return DeleteCashierMutation(success=bool(cashier))


class CreateClasificationMutation(relay.ClientIDMutation):
    class Input:
        account_id = graphene.ID(required=True)
        name = graphene.String(required=True)

    clasification = graphene.Field(ClasificationNode)
    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, account_id, name, client_mutation_id=None):
        account = Node.get_node_from_global_id(info, account_id)
        name = name

        clasification = Clasification.objects.filter(account=account, name=name).first()

        assert clasification is None, 'Clasification exists: {0}'.format(
            Node.to_global_id('ClasificationNode', clasification.id)
        )

        clasification = Clasification.objects.create(account=account, name=name)
        success = True

        return CreateClasificationMutation(clasification=clasification, success=success)


class DeleteClasificationMutation(relay.ClientIDMutation):
    class Input:
        clasification_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, clasification_id):
        clasification = Node.get_node_from_global_id(info, clasification_id)

        assert clasification is not None, 'Clasification not Exists'

        clasification.delete()
        return DeleteClasificationMutation(success=bool(clasification))


class Mutation(object):

    create_account = CreateAccountMutation.Field()
    delete_account = DeleteAccountMutation.Field()

    create_cashier = CreateCashierMutation.Field()
    delete_cashier = DeleteCashierMutation.Field()

    create_clasification = CreateClasificationMutation.Field()
    delete_clasification = DeleteClasificationMutation.Field()
