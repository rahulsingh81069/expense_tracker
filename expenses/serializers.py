from rest_framework import serializers

from .models import Expense, Split, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'mobile_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  
        user.save()
        return user


class SplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Split
        fields = ['user', 'amount', 'percentage']

class ExpenseSerializer(serializers.ModelSerializer):
    splits = SplitSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'payer', 'split_method', 'splits']
    
    def validate(self, data):
        if data['split_method'] == 'exact':
            if sum(split['amount'] for split in data['splits']) != data['amount']:
                raise serializers.ValidationError("Total split amounts must equal the total expense amount.")
        elif data['split_method'] == 'percentage':
            if sum(split['percentage'] for split in data['splits']) != 100:
                raise serializers.ValidationError("Total percentages must equal 100.")
        return data


    def create(self, validated_data):
        splits_data = validated_data.pop('splits')
        expense = Expense.objects.create(**validated_data)
        self.handle_splits(expense, splits_data, validated_data['split_method'])
        return expense

    def handle_splits(self, expense, splits_data, split_method):
        total_amount = expense.amount
        if split_method == 'equal':
            num_splits = len(splits_data)
            split_amount = total_amount / num_splits
            for split_data in splits_data:
                Split.objects.create(expense=expense, user_id=split_data['user_id'], amount=split_amount)
        elif split_method == 'exact':
            for split_data in splits_data:
                Split.objects.create(expense=expense, user_id=split_data['user_id'], amount=split_data['amount'])
        elif split_method == 'percentage':
            for split_data in splits_data:
                amount = (total_amount * split_data['percentage']) / 100
                Split.objects.create(expense=expense, user_id=split_data['user_id'], amount=amount)
    splits = SplitSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'payer', 'split_method', 'splits']

    def create(self, validated_data):
        splits_data = validated_data.pop('splits')
        expense = Expense.objects.create(**validated_data)
        for split_data in splits_data:
            Split.objects.create(expense=expense, **split_data)
        return expense
