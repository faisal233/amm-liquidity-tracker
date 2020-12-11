"""
This is the tokens module and supports all the REST actions for the
tokens data
"""

from flask import make_response, abort

from config import db
from models import Token, TokenSchema


def read_all():
    """
    This function responds to a request for /api/tokens
    with the complete lists of tokens

    :return:        json string of list of tokens
    """
    # Create the list of tokens from our dataread
    tokens = Token.query.order_by(Token.total_usd_value.desc()).all()

    # Serialize the data for the response
    token_schema = TokenSchema(many=True)
    data = token_schema.dump(tokens).data
    return data


def read_one(token_id):
    """
    This function responds to a request for /api/tokens/{token_id}
    with one matching token from tokens

    :param token_id:   Id of token to find
    :return:            token matching id
    """
    # Build the initial query
    token = Token.query.get(token_id)

    # Did we find a Token?
    if token is not None:
        # Serialize the data for the response
        token_schema = TokenSchema()
        data = token_schema.dump(token).data
        return data

    # Otherwise, nope, didn't find that token
    else:
        abort(404, f"token not found for Id: {token_id}")


def create(token):
    """
    This function creates a new token in the tokens structure
    based on the passed in token data

    :param token:  token to create in tokens structure
    :return:        201 on success, 406 on token exists
    """

    token_id = token.get("id")

    existing_token = Token.query.filter(Token.token_id == token_id)

    # Can we insert this token?
    if existing_token is None:

        # Create a token instance using the schema and the passed in token
        schema = TokenSchema()
        new_token = schema.load(token, session=db.session).data

        # Add the token to the database
        db.session.add(new_token)
        db.session.commit()

        # Serialize and return the newly created token in the response
        data = schema.dump(new_token).data

        return data, 201

    # Otherwise, nope, token exists already
    else:
        abort(409, f"token {token_id} exists already")


def update(token_id, token):
    """
    This function updates an existing token in the tokens structure

    :param token_id:   Id of the token to update in the tokens structure
    :param token:      token to update
    :return:            updated token structure
    """
    # Get the Token requested from the db into session
    update_token = Token.query.filter(Token.token_id == token_id).one_or_none()

    # Did we find an existing token?
    if update_token is not None:

        # turn the passed in token into a db object
        schema = TokenSchema()
        up_date = schema.load(token, session=db.session).data

        # Set the id to the token we want to update
        up_date.token_id = update_token.token_id

        # merge the new object into the old and commit it to the db
        db.session.merge(up_date)
        db.session.commit()

        # return updated token in the response
        data = schema.dump(update_token).data

        return data, 200

    # Otherwise, nope, didn't find that token
    else:
        abort(404, f"token not found for Id: {token_id}")


def delete(token_id):
    """
    This function deletes a token from the tokens structure

    :param token_id:   Id of the token to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the token requested
    token = Token.query.filter(Token.token_id == token_id).one_or_none()

    # Did we find a Token?
    if token is not None:
        db.session.delete(token)
        db.session.commit()
        return make_response(f"token {token_id} deleted", 200)

    # Otherwise, nope, didn't find that token
    else:
        abort(404, f"token not found for Id: {token_id}")
