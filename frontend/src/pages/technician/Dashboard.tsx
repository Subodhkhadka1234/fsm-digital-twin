import React, { useEffect, useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Box,
  List,
  ListItem,
  ListItemText,
  Button,
} from '@mui/material';
import {
  Work as WorkIcon,
  CheckCircle as CompletedIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import apiService from '../../services/api';

interface TechnicianDashboardData {
  today_jobs: number;
  completed_today: number;
  on_time_percentage: number;
  rating: number;
}

const TechnicianDashboard: React.FC = () => {
  const [stats, setStats] = useState<TechnicianDashboardData | null>(null);
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const [dashboardData, jobsData] = await Promise.all([
        apiService.getTechnicianDashboard(),
        apiService.getTechnicianJobs('scheduled'),
      ]);
      setStats(dashboardData);
      setJobs(jobsData);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Technician Dashboard
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <div>
                  <Typography color="textSecondary" gutterBottom>
                    Today's Jobs
                  </Typography>
                  <Typography variant="h4">{stats?.today_jobs || 0}</Typography>
                </div>
                <WorkIcon color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <div>
                  <Typography color="textSecondary" gutterBottom>
                    Completed Today
                  </Typography>
                  <Typography variant="h4">{stats?.completed_today || 0}</Typography>
                </div>
                <CompletedIcon color="success" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <div>
                  <Typography color="textSecondary" gutterBottom>
                    On-Time Rate
                  </Typography>
                  <Typography variant="h4">
                    {stats?.on_time_percentage || 0}%
                  </Typography>
                </div>
                <ScheduleIcon color="info" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Today's Schedule
            </Typography>
            {jobs.length === 0 ? (
              <Typography color="textSecondary">No scheduled jobs for today</Typography>
            ) : (
              <List>
                {jobs.map((job: any) => (
                  <ListItem
                    key={job.id}
                    secondaryAction={
                      <Button variant="contained" size="small">
                        Start
                      </Button>
                    }
                  >
                    <ListItemText
                      primary={job.job_type}
                      secondary={`${job.address} - Priority: ${job.priority}`}
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default TechnicianDashboard;
