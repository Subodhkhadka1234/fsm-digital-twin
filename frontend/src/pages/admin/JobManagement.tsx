import React, { useEffect, useState } from 'react';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Chip,
  Typography,
  Box,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import apiService from '../../services/api';
import { Job } from '../../types';

const JobManagement: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    try {
      const data = await apiService.getJobs();
      setJobs(data);
    } catch (error) {
      console.error('Failed to load jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: { [key: string]: any } = {
      pending: 'warning',
      scheduled: 'info',
      in_progress: 'primary',
      completed: 'success',
      cancelled: 'error',
    };
    return colors[status] || 'default';
  };

  const getPriorityColor = (priority: string) => {
    const colors: { [key: string]: any } = {
      low: 'default',
      medium: 'info',
      high: 'warning',
      emergency: 'error',
    };
    return colors[priority] || 'default';
  };

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Job Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {/* TODO: Open create job dialog */}}
        >
          Create Job
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Job Type</TableCell>
              <TableCell>Customer</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Priority</TableCell>
              <TableCell>Address</TableCell>
              <TableCell>Scheduled</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {jobs.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center">
                  No jobs found
                </TableCell>
              </TableRow>
            ) : (
              jobs.map((job) => (
                <TableRow key={job.id}>
                  <TableCell>{job.job_type}</TableCell>
                  <TableCell>{job.customer_id}</TableCell>
                  <TableCell>
                    <Chip
                      label={job.status}
                      color={getStatusColor(job.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={job.priority}
                      color={getPriorityColor(job.priority)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{job.address}</TableCell>
                  <TableCell>
                    {job.scheduled_start
                      ? new Date(job.scheduled_start).toLocaleDateString()
                      : '-'}
                  </TableCell>
                  <TableCell>
                    <Button size="small">View</Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default JobManagement;
