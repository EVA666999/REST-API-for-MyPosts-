import base64

from django.core.files.base import ContentFile
from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith("data:image"):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(";base64,")
            # И извлечь расширение файла.
            ext = format.split("/")[-1]
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = "__all__"
        many = True


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = "__all__"
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Group


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("author", "post")


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        exclude = ("id",)

    def validate(self, data):
        if data["user"] == data["following"]:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя!"
            )
        return data
