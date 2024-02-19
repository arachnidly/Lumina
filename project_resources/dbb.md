# db info

Here's how you can perform CRUD operations on the `User` and `Article` models using SQLAlchemy:

1. **Create**

    ```python
    from models import User, Article, db

    # Create a new user
    new_user = User(username='username', email='email@example.com')
    db.session.add(new_user)
    db.session.commit()

    # Create a new article
    new_article = Article(title='title', content='content')
    db.session.add(new_article)
    db.session.commit()
    ```

1. **Read**

    ```python
    # Get all users
    users = User.query.all()

    # Get user by id
    user = User.query.get(user_id)

    # Get all articles
    articles = Article.query.all()

    # Get article by id
    article = Article.query.get(article_id)
    ```

1. **Update**

    ```python
    # Update a user
    user = User.query.get(user_id)
    user.username = 'new_username'
    db.session.commit()

    # Update an article
    article = Article.query.get(article_id)
    article.title = 'new_title'
    db.session.commit()
    ```

1. **Delete**

    ```python
    # Delete a user
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    # Delete an article
    article = Article.query.get(article_id)
    db.session.delete(article)
    db.session.commit()
    ```

Remember to replace `'username'`, `'email@example.com'`, `'title'`, `'content'`, `'new_username'`, `'new_title'`, `user_id`, and `article_id` with your actual data or variables. Also, make sure to handle exceptions and errors as necessary.
