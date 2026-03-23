"""
FastAPI backend tests using AAA (Arrange-Act-Assert) pattern.
"""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, fresh_activities):
        """Test that GET /activities returns all activities."""
        # Arrange
        expected_activity_count = 3

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert len(response.json()) == expected_activity_count
        assert "Chess Club" in response.json()


class TestSignupForActivity:
    """Tests for POST /activities/{activity}/signup endpoint."""

    def test_signup_successful(self, client, fresh_activities):
        """Test successful signup for an activity."""
        # Arrange
        activity = "Gym Class"
        email = "newstudent@test.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity}"

    def test_signup_duplicate_student_returns_400(self, client, fresh_activities):
        """Test that signing up twice for the same activity returns 400."""
        # Arrange
        activity = "Chess Club"
        email = "alice@test.edu"  # Already in participants

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_invalid_activity_returns_404(self, client, fresh_activities):
        """Test that signing up for non-existent activity returns 404."""
        # Arrange
        activity = "Fake Club"
        email = "student@test.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestRemoveFromActivity:
    """Tests for DELETE /activities/{activity}/participant/{email} endpoint."""

    def test_remove_participant_successful(self, client, fresh_activities):
        """Test successful removal of a participant."""
        # Arrange
        activity = "Chess Club"
        email = "alice@test.edu"  # Existing participant

        # Act
        response = client.delete(
            f"/activities/{activity}/participant/{email}"
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity}"

    def test_remove_nonexistent_participant_returns_404(self, client, fresh_activities):
        """Test that removing non-existent participant returns 404."""
        # Arrange
        activity = "Chess Club"
        email = "nonexistent@test.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/participant/{email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_remove_from_invalid_activity_returns_404(self, client, fresh_activities):
        """Test that removing from non-existent activity returns 404."""
        # Arrange
        activity = "Fake Club"
        email = "student@test.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/participant/{email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
