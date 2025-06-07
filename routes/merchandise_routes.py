from flask import Blueprint, request, jsonify
from models.merchandise import (
    insert_product, get_all_products, get_products_by_club, update_product,
    create_order, get_all_orders, get_orders_by_club, update_order_status,
    get_dashboard_stats,delete_product
)


merchandise_bp = Blueprint('merchandise', __name__)


# ------------------- Product Routes -------------------

@merchandise_bp.route('/products', methods=['POST'])
def add_product():
    """Add a new product."""
    try:
        data = request.get_json()
        result = insert_product(data)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@merchandise_bp.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    """Delete a product by ID."""
    try:
        result = delete_product(product_id)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@merchandise_bp.route('/products', methods=['GET'])
def list_products():
    """List all products."""
    try:
        result = get_all_products()
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@merchandise_bp.route('/products/club/<club_id>', methods=['GET'])
def list_products_by_club(club_id):
    """List products by club ID."""
    try:
        result = get_products_by_club(club_id)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@merchandise_bp.route('/products/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    """Update a product."""
    try:
        data = request.get_json()
        result = update_product(product_id, data)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ------------------- Order Routes -------------------

@merchandise_bp.route('/orders', methods=['POST'])
def place_order():
    """Create a new order."""
    try:
        data = request.get_json()
        result = create_order(data)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@merchandise_bp.route('/orders', methods=['GET'])
def list_orders():
    """Get all orders."""
    try:
        result = get_all_orders()
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@merchandise_bp.route('/orders/club/<club_id>', methods=['GET'])
def list_orders_by_club(club_id):
    """Get all orders by club ID."""
    try:
        result = get_orders_by_club(club_id)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@merchandise_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def change_order_status(order_id):
    """Update an order's status."""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        result = update_order_status(order_id, data['status'])
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ------------------- Dashboard Route -------------------

@merchandise_bp.route('/dashboard/<club_id>', methods=['GET'])
def dashboard_summary(club_id):
    """Dashboard stats for a club."""
    try:
        result = get_dashboard_stats(club_id)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
