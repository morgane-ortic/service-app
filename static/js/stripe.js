// Initialize Stripe
const stripe = Stripe('pk_test_51QfanDL2WsViswULccd4To2itF8MFURItNqzarLl6E1x5G7oS6aAMq9ItT0HmQMtyP3bDkh3xXtlKhCr49Ux1Z0E00mp1KFLCj');

document.addEventListener('DOMContentLoaded', () => {
    const stripePayButton = document.getElementById('stripe_pay_button');

    if (stripePayButton) {
        stripePayButton.addEventListener('click', () => {
            fetch('/customers/create-checkout-session/', {  // Update if necessary
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                credentials: 'same-origin',
            })
                .then(response => {
                    if (!response.ok) throw new Error('Failed to create Stripe Checkout session.');
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        return stripe.redirectToCheckout({ sessionId: data.id });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Something went wrong while processing your payment.');
                });
        });
    }
});
