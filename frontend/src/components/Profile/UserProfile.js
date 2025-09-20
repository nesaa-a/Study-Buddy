import React from 'react';
import './UserProfile.css';

const UserProfile = ({ user }) => {
  return (
    <div className="profile-container">
      <div className="profile-card">
        <div className="profile-header">
          <div className="profile-avatar">
            {user.username.charAt(0).toUpperCase()}
          </div>
          <h2>👤 Profile</h2>
        </div>
        
        <div className="profile-info">
          <div className="info-section">
            <h3>Account Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Username</label>
                <span>{user.username}</span>
              </div>
              <div className="info-item">
                <label>Email</label>
                <span>{user.email}</span>
              </div>
              <div className="info-item">
                <label>Full Name</label>
                <span>{user.full_name || 'Not provided'}</span>
              </div>
              <div className="info-item">
                <label>Member Since</label>
                <span>{new Date(user.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
          
          <div className="info-section">
            <h3>Account Status</h3>
            <div className="status-item">
              <span className="status-label">Status</span>
              <span className={`status-badge ${user.is_active === 'true' ? 'active' : 'inactive'}`}>
                {user.is_active === 'true' ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>
          
          <div className="info-section">
            <h3>Study Statistics</h3>
            <div className="stats-grid">
              <div className="stat-item">
                <div className="stat-number">0</div>
                <div className="stat-label">Documents Uploaded</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">0</div>
                <div className="stat-label">Study Sessions</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">0</div>
                <div className="stat-label">Hours Studied</div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="profile-actions">
          <button className="action-button edit-button">
            ✏️ Edit Profile
          </button>
          <button className="action-button settings-button">
            ⚙️ Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
